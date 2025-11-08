from datetime import datetime

def get_share_price(symbol: str):
    """
    Mock price feed for demo/testing.
    Extend/replace with real API if needed.
    """
    sym = str(symbol).upper().strip()
    prices = {
        "AAPL": 150.0,
        "TSLA": 700.0,
        "GOOGL": 2800.0
    }
    return prices.get(sym)

class Account:
    def __init__(self, initial_balance):
        self.balance = float(initial_balance)
        self.shares = {}
        self.transactions = []

    def _now(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _normalize_symbol(self, symbol):
        return str(symbol).upper().strip()

    def _append_txn(self, **txn):
        txn["balance"] = round(self.balance, 2)
        self.transactions.append(txn)

    def deposit_funds(self, amount):
        amt = float(amount)
        if amt <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance = round(self.balance + amt, 2)
        self._append_txn(ts=self._now(), type="DEPOSIT", symbol=None, qty=0,
                         price=None, amount=amt, note="Funds deposited")

    def withdraw_funds(self, amount):
        amt = float(amount)
        if amt <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance - amt < 0:
            raise ValueError("Insufficient balance for withdrawal.")
        self.balance = round(self.balance - amt, 2)
        self._append_txn(ts=self._now(), type="WITHDRAW", symbol=None, qty=0,
                         price=None, amount=-amt, note="Funds withdrawn")

    def buy_shares(self, symbol, quantity):
        sym = self._normalize_symbol(symbol)
        qty = int(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be positive.")
        price = get_share_price(sym)
        if price is None:
            raise ValueError(f"Unknown symbol: {sym}")
        cost = round(price * qty, 2)
        if self.balance < cost:
            raise ValueError("Insufficient balance.")
        self.balance = round(self.balance - cost, 2)
        self.shares[sym] = int(self.shares.get(sym, 0)) + qty
        self._append_txn(ts=self._now(), type="BUY", symbol=sym, qty=qty,
                         price=price, amount=-cost, note=f"Bought {qty} {sym}")

    def sell_shares(self, symbol, quantity):
        sym = self._normalize_symbol(symbol)
        qty = int(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be positive.")
        current_qty = int(self.shares.get(sym, 0))
        if current_qty < qty:
            raise ValueError("Not enough shares to sell.")
        price = get_share_price(sym)
        if price is None:
            raise ValueError(f"Unknown symbol: {sym}")
        proceeds = round(price * qty, 2)
        self.balance = round(self.balance + proceeds, 2)
        new_qty = current_qty - qty
        if new_qty > 0:
            self.shares[sym] = new_qty
        else:
            self.shares.pop(sym, None)
        self._append_txn(ts=self._now(), type="SELL", symbol=sym, qty=qty,
                         price=price, amount=proceeds, note=f"Sold {qty} {sym}")

    def calculate_portfolio_value(self):
        total_value = float(self.balance)
        for sym, qty in self.shares.items():
            price = get_share_price(sym)
            if price:
                total_value += price * qty
        return round(total_value, 2)

    def calculate_profit_loss(self, initial_deposit):
        return round(self.calculate_portfolio_value() - float(initial_deposit), 2)

    def report_holdings(self):
        return {sym: int(qty) for sym, qty in self.shares.items()}

    def list_transactions(self):
        return list(self.transactions)
