import gradio as gr
import pandas as pd
from inventory import InventoryManager, ValidationError

inv = InventoryManager()

# ---------- HANDLERS ----------
def add_item_handler(item_id, name, category, quantity, price, supplier, reorder_threshold):
    try:
        msg = inv.add_item(
            item_id=item_id,
            name=name,
            category=category,
            quantity=quantity,
            price=price,
            supplier=supplier,
            reorder_threshold=reorder_threshold,
        )
        return msg
    except ValidationError as e:
        return f"❌ {e}"

def update_item_handler(item_id, name, category, quantity, price, supplier, reorder_threshold):
    try:
        fields = {}
        if name: fields["name"] = name
        if category: fields["category"] = category
        if quantity not in (None, ""): fields["quantity"] = quantity
        if price not in (None, ""): fields["price"] = price
        if supplier: fields["supplier"] = supplier
        if reorder_threshold not in (None, ""): fields["reorder_threshold"] = reorder_threshold
        msg = inv.update_item(int(item_id), **fields)
        return msg
    except ValidationError as e:
        return f"❌ {e}"

def delete_item_handler(item_id):
    try:
        msg = inv.delete_item(int(item_id))
        return msg
    except ValidationError as e:
        return f"❌ {e}"

def view_item_handler(item_id):
    item = inv.get_item(int(item_id))
    if not item:
        return pd.DataFrame([{"message": "Item not found"}])
    return pd.DataFrame([item])

def list_items_handler():
    return pd.DataFrame(inv.list_items())

def search_items_handler(key, value):
    return pd.DataFrame(inv.search_items(key, value))

def reports_overview_handler():
    df_low = pd.DataFrame(inv.low_stock())
    total = inv.total_value()
    return df_low, f"💰 Total Inventory Value: {total:.2f}"

def download_pdf_handler():
    ok, path = inv.export_pdf()
    if ok:
        return path
    raise gr.Error(path)

# ---------- THEME + LAYOUT ----------
theme = gr.themes.Soft(
    primary_hue="orange",
    neutral_hue="slate",
    font=["Inter", "sans-serif"],
    radius_size="md",
    spacing_size="md",
)

css = """
.gradio-container { max-width: 1100px; margin: auto; }
h1, h2, h3 { color: #ea580c !important; }
button { border-radius: 8px !important; }
"""

with gr.Blocks(theme=theme, css=css, title="Inventory Management System") as demo:
    gr.Markdown("# 📦 Inventory Management System\nManage, search, and report on your stock.")

    # --- Add Item ---
    with gr.Tab("➕ Add Item"):
        with gr.Row():
            with gr.Column(scale=3):
                item_id = gr.Number(label="Item ID", precision=0)
                name = gr.Textbox(label="Name")
                category = gr.Textbox(label="Category")
                quantity = gr.Number(label="Quantity", precision=0)
                price = gr.Number(label="Price")
                supplier = gr.Textbox(label="Supplier")
                reorder = gr.Number(label="Reorder Threshold", precision=0)
                add_btn = gr.Button("Add Item", variant="primary")
                clear_btn = gr.Button("Clear Form")
            add_output = gr.Textbox(label="Status", interactive=False)
        add_btn.click(add_item_handler, [item_id, name, category, quantity, price, supplier, reorder], add_output)
        clear_btn.click(lambda: (None, "", "", None, None, "", None, ""), outputs=[item_id, name, category, quantity, price, supplier, reorder, add_output])

    # --- Update Item ---
    with gr.Tab("✏️ Update Item"):
        with gr.Row():
            with gr.Column(scale=3):
                u_item_id = gr.Number(label="Item ID", precision=0)
                u_name = gr.Textbox(label="Name (optional)")
                u_category = gr.Textbox(label="Category (optional)")
                u_quantity = gr.Number(label="Quantity (optional)", precision=0)
                u_price = gr.Number(label="Price (optional)")
                u_supplier = gr.Textbox(label="Supplier (optional)")
                u_reorder = gr.Number(label="Reorder Threshold (optional)", precision=0)
                update_btn = gr.Button("Update", variant="primary")
            update_output = gr.Textbox(label="Status", interactive=False)
        update_btn.click(update_item_handler, [u_item_id, u_name, u_category, u_quantity, u_price, u_supplier, u_reorder], update_output)

    # --- Delete Item ---
    with gr.Tab("🗑️ Delete Item"):
        d_item_id = gr.Number(label="Item ID", precision=0)
        delete_btn = gr.Button("Delete", variant="stop")
        delete_output = gr.Textbox(label="Status", interactive=False)
        delete_btn.click(delete_item_handler, d_item_id, delete_output)

    # --- View Single Item ---
    with gr.Tab("🔍 View Item"):
        v_item_id = gr.Number(label="Item ID", precision=0)
        view_btn = gr.Button("Fetch Item")
        table_single = gr.Dataframe(label="Item Details", interactive=False)
        view_btn.click(view_item_handler, v_item_id, table_single)

    # --- Browse / Search ---
    with gr.Tab("📋 Browse & Search"):
        refresh_btn = gr.Button("Refresh List", variant="secondary")
        all_table = gr.Dataframe(label="All Items", interactive=False)
        with gr.Row():
            key = gr.Dropdown(["name", "category", "supplier"], label="Search by", value="name")
            value = gr.Textbox(label="Search Query")
            search_btn = gr.Button("Search", variant="primary")
        search_results = gr.Dataframe(label="Search Results", interactive=False)
        refresh_btn.click(list_items_handler, outputs=all_table)
        search_btn.click(search_items_handler, [key, value], outputs=search_results)

    # --- Reports ---
    with gr.Tab("📊 Reports"):
        with gr.Row():
            overview_btn = gr.Button("Show Overview", variant="secondary")
            pdf_btn = gr.Button("Download PDF", variant="primary")
        low_stock_df = gr.Dataframe(label="Low Stock Items", interactive=False)
        total_value_box = gr.Textbox(label="Summary", interactive=False)
        pdf_file = gr.File(label="PDF Report", interactive=False)
        overview_btn.click(reports_overview_handler, outputs=[low_stock_df, total_value_box])
        pdf_btn.click(download_pdf_handler, outputs=pdf_file)

demo.launch(share=True)
