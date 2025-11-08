
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os

# Optional dependency for PDF reports
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False


ALLOWED_KEYS = {"item_id", "name", "category", "quantity", "price", "supplier", "reorder_threshold"}


class ValidationError(Exception):
    pass


def _validate_item(item: Dict):
    required = ["item_id", "name", "category", "quantity", "price", "supplier", "reorder_threshold"]
    missing = [k for k in required if k not in item or item[k] in (None, "")]
    if missing:
        raise ValidationError(f"Missing required fields: {', '.join(missing)}")
    try:
        item["item_id"] = int(item["item_id"])
    except Exception:
        raise ValidationError("item_id must be an integer")
    for k in ("quantity", "reorder_threshold"):
        try:
            item[k] = int(item[k])
            if item[k] < 0:
                raise ValidationError(f"{k} cannot be negative")
        except ValueError:
            raise ValidationError(f"{k} must be an integer")
    try:
        item["price"] = float(item["price"])
        if item["price"] < 0:
            raise ValidationError("price cannot be negative")
    except ValueError:
        raise ValidationError("price must be a number")
    # normalize strings
    for k in ("name", "category", "supplier"):
        item[k] = str(item[k]).strip()
        if not item[k]:
            raise ValidationError(f"{k} cannot be empty")
    return item


class InventoryManager:
    def __init__(self, db_path: str = "inventory.db", audit_path: str = "audit.log"):
        self.db_path = db_path
        self.audit_path = audit_path
        self._ensure_tables()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def _ensure_tables(self):
        with self._conn() as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS items(
                    item_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    supplier TEXT NOT NULL,
                    reorder_threshold INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    def _audit(self, action: str, payload: Dict):
        entry = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "payload": payload,
        }
        with open(self.audit_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    # CRUD
    def add_item(self, **item) -> str:
        item = _validate_item(item)
        with self._conn() as con:
            cur = con.execute("SELECT 1 FROM items WHERE item_id=?", (item["item_id"],))
            if cur.fetchone():
                raise ValidationError(f"Item with id {item['item_id']} already exists")
            now = datetime.utcnow().isoformat()
            con.execute(
                """INSERT INTO items(item_id,name,category,quantity,price,supplier,reorder_threshold,created_at,updated_at)
                   VALUES(?,?,?,?,?,?,?,?,?)""",
                (
                    item["item_id"],
                    item["name"],
                    item["category"],
                    item["quantity"],
                    item["price"],
                    item["supplier"],
                    item["reorder_threshold"],
                    now,
                    now,
                ),
            )
        self._audit("create", item)
        return "Item added successfully"

    def update_item(self, item_id: int, **fields) -> str:
        if not fields:
            raise ValidationError("Provide at least one field to update")
        # validate fields types
        updates = {}
        for k, v in fields.items():
            if k not in ALLOWED_KEYS or k == "item_id" or v in (None, ""):
                continue
            if k in ("quantity", "reorder_threshold"):
                try:
                    v = int(v)
                    if v < 0:
                        raise ValidationError(f"{k} cannot be negative")
                except ValueError:
                    raise ValidationError(f"{k} must be an integer")
            elif k == "price":
                try:
                    v = float(v)
                    if v < 0:
                        raise ValidationError("price cannot be negative")
                except ValueError:
                    raise ValidationError("price must be a number")
            else:
                v = str(v).strip()
                if not v:
                    raise ValidationError(f"{k} cannot be empty")
            updates[k] = v
        if not updates:
            raise ValidationError("No valid fields to update")
        sets = ", ".join(f"{k}=?" for k in updates.keys())
        params = list(updates.values())
        params.append(item_id)
        with self._conn() as con:
            cur = con.execute("SELECT 1 FROM items WHERE item_id=?", (item_id,))
            if not cur.fetchone():
                raise ValidationError(f"Item with id {item_id} not found")
            con.execute(f"UPDATE items SET {sets}, updated_at=? WHERE item_id=?", (*updates.values(), datetime.utcnow().isoformat(), item_id))
        self._audit("update", {"item_id": item_id, "fields": updates})
        return "Item updated successfully"

    def delete_item(self, item_id: int) -> str:
        with self._conn() as con:
            cur = con.execute("DELETE FROM items WHERE item_id=?", (item_id,))
            if cur.rowcount == 0:
                raise ValidationError(f"Item with id {item_id} not found")
        self._audit("delete", {"item_id": item_id})
        return "Item deleted successfully"

    def get_item(self, item_id: int) -> Optional[Dict]:
        with self._conn() as con:
            cur = con.execute("SELECT * FROM items WHERE item_id=?", (item_id,))
            row = cur.fetchone()
        return self._row_to_dict(row) if row else None

    def list_items(self) -> List[Dict]:
        with self._conn() as con:
            cur = con.execute("SELECT * FROM items ORDER BY item_id")
            rows = cur.fetchall()
        return [self._row_to_dict(r) for r in rows]

    def search_items(self, key: str, value: str) -> List[Dict]:
        key = key if key in ("name", "category", "supplier") else "name"
        q = f"SELECT * FROM items WHERE {key} LIKE ? ORDER BY item_id"
        with self._conn() as con:
            rows = con.execute(q, (f"%{value.strip()}%",)).fetchall()
        return [self._row_to_dict(r) for r in rows]

    def low_stock(self) -> List[Dict]:
        with self._conn() as con:
            rows = con.execute("SELECT * FROM items WHERE quantity <= reorder_threshold ORDER BY item_id").fetchall()
        return [self._row_to_dict(r) for r in rows]

    def total_value(self) -> float:
        with self._conn() as con:
            val = con.execute("SELECT SUM(quantity * price) FROM items").fetchone()[0]
        return float(val or 0.0)

    def export_pdf(self, filepath: str = "inventory_report.pdf") -> Tuple[bool, str]:
        if not REPORTLAB_AVAILABLE:
            return False, "reportlab not installed. Install with: pip install reportlab"
        items = self.list_items()
        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4
        y = height - 2*cm
        c.setFont("Helvetica-Bold", 16)
        c.drawString(2*cm, y, "Inventory Report")
        y -= 1*cm
        c.setFont("Helvetica", 10)
        c.drawString(2*cm, y, f"Generated: {datetime.utcnow().isoformat()}Z")
        y -= 1*cm
        headers = ["ID", "Name", "Category", "Qty", "Price", "Supplier", "Reorder"]
        col_x = [2*cm, 4*cm, 9*cm, 13*cm, 15*cm, 17*cm, 19*cm]
        c.setFont("Helvetica-Bold", 10)
        for i, h in enumerate(headers):
            c.drawString(col_x[i], y, h)
        y -= 0.5*cm
        c.setFont("Helvetica", 10)
        for it in items:
            if y < 2*cm:
                c.showPage()
                y = height - 2*cm
            row = [str(it["item_id"]), it["name"], it["category"], str(it["quantity"]), f"{it['price']:.2f}", it["supplier"], str(it["reorder_threshold"])]
            for i, cell in enumerate(row):
                c.drawString(col_x[i], y, cell[:24])
            y -= 0.5*cm
        y -= 0.5*cm
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2*cm, y, f"Total Inventory Value: {self.total_value():.2f}")
        y -= 0.7*cm
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2*cm, y, "Low Stock Items:")
        y -= 0.5*cm
        c.setFont("Helvetica", 10)
        for it in self.low_stock():
            if y < 2*cm:
                c.showPage()
                y = height - 2*cm
            c.drawString(2*cm, y, f"- {it['name']} (qty {it['quantity']}, reorder @ {it['reorder_threshold']})")
            y -= 0.4*cm
        c.showPage()
        c.save()
        return True, filepath

    @staticmethod
    def _row_to_dict(row) -> Dict:
        keys = ["item_id","name","category","quantity","price","supplier","reorder_threshold","created_at","updated_at"]
        return {k: row[i] for i, k in enumerate(keys)}
