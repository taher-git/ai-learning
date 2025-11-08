class Account:
    def __init__(self, initial_balance):
        self.balance = initial_balance
        self.shares = {}
        self.transactions = []

    def deposit_funds(self, amount):
        """Deposit funds into the account."""
        self.balance += amount

    def withdraw_funds(self, amount):
        """Withdraw funds from the account, preventing negative balance."""
        if self.balance - amount >= 0:
            self.balance -= amount
        else:
            print("Error: Insufficient balance for withdrawal.")

    def buy_shares(self, symbol, quantity):
        """Record buying of shares, verifying affordability."""
        share_price = get_share_price(symbol)
        if share_price is not None and self.balance >= share_price * quantity:
            self.balance -= share_price * quantity
            if symbol in self.shares:
                self.shares[symbol] += quantity
            else:
                self.shares[symbol] = quantity
            self.transactions.append(f"Bought {quantity} shares of {symbol} at ${share_price}")

    def sell_shares(self, symbol, quantity):
        """Record selling of shares, ensuring sufficient shares to sell."""
        if symbol in self.shares and self.shares[symbol] >= quantity:
            share_price = get_share_price(symbol)
            self.balance += share_price * quantity
            self.shares[symbol] -= quantity
            self.transactions.append(f"Sold {quantity} shares of {symbol} at ${share_price}")

    def calculate_portfolio_value(self):
        """Calculate the total value of the user's portfolio."""
        total_value = self.balance
        for symbol, quantity in self.shares.items():
            share_price = get_share_price(symbol)
            if share_price is not None:
                total_value += share_price * quantity
        return total_value

    def calculate_profit_loss(self, initial_deposit):
        """Calculate the profit or loss from the initial deposit."""
        return self.calculate_portfolio_value() - initial_deposit

    def report_holdings(self):
        """Report the holdings of the user at any point in time."""
        return self.shares

    def report_profit_loss(self, initial_deposit):
        """Report the profit or loss of the user at any point in time."""
        return self.calculate_profit_loss(initial_deposit)

    def list_transactions(self):
        """List all the transactions that the user has made over time."""
        return self.transactions

def get_share_price(symbol):
    """Mock function to get share price for testing."""
    if symbol == 'AAPL':
        return 150
    elif symbol == 'TSLA':
        return 700
    elif symbol == 'GOOGL':
        return 2800
    else:
        return None

from accounts import Account, get_share_price
import unittest

class TestAccountMethods(unittest.TestCase):

    def test_deposit_funds(self):
        acc = Account(1000)
        acc.deposit_funds(500)
        self.assertEqual(acc.balance, 1500)
    
    def test_withdraw_funds_sufficient_balance(self):
        acc = Account(1000)
        acc.withdraw_funds(200)
        self.assertEqual(acc.balance, 800)
    
    def test_withdraw_funds_insufficient_balance(self):
        acc = Account(1000)
        acc.withdraw_funds(1200)
        self.assertEqual(acc.balance, 1000)
    
    def test_buy_shares(self):
        acc = Account(1000)
        acc.buy_shares('AAPL', 2)
        self.assertEqual(acc.balance, 1500)
        self.assertEqual(acc.shares['AAPL'], 2)
    
    def test_sell_shares(self):
        acc = Account(1000)
        acc.buy_shares('AAPL', 2)
        acc.sell_shares('AAPL', 1)
        self.assertEqual(acc.balance, 1650)
        self.assertEqual(acc.shares['AAPL'], 1)
    
    def test_calculate_portfolio_value(self):
        acc = Account(1000)
        acc.buy_shares('AAPL', 2)
        acc.buy_shares('TSLA', 1)
        self.assertEqual(acc.calculate_portfolio_value(), 2050)
    
    def test_calculate_profit_loss(self):
        acc = Account(1000)
        acc.buy_shares('AAPL', 2)
        self.assertEqual(acc.calculate_profit_loss(1000), 150)
    
    def test_report_holdings(self):
        acc = Account(1000)
        acc.buy_shares('AAPL', 2)
        self.assertEqual(acc.report_holdings(), {'AAPL': 2})
    
    def test_report_profit_loss(self):
        acc = Account(1000)
        acc.buy_shares('AAPL', 2)
        self.assertEqual(acc.report_profit_loss(1000), 150)
    
    def test_list_transactions(self):
        acc = Account(1000)
        acc.buy_shares('AAPL', 2)
        acc.sell_shares('AAPL', 1)
        self.assertEqual(acc.list_transactions(), ['Bought 2 shares of AAPL at $150', 'Sold 1 shares of AAPL at $150'])

if __name__ == '__main__':
    unittest.main()