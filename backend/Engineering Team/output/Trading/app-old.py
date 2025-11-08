import gradio as gr
from accounts import Account, get_share_price

# Initialize global account
account = Account(1000)

# --- Business logic functions ---
def create_account(initial_balance):
    global account
    account = Account(initial_balance)
    return f"Account created with initial balance: ${initial_balance}"

def deposit_funds(amount):
    account.deposit_funds(amount)
    return f"Deposited ${amount}. New balance: ${account.balance}"

def withdraw_funds(amount):
    account.withdraw_funds(amount)
    return f"Withdrew ${amount}. New balance: ${account.balance}"

def buy_shares(symbol, quantity):
    account.buy_shares(symbol, quantity)
    return f"Bought {quantity} shares of {symbol}. New balance: ${account.balance}"

def sell_shares(symbol, quantity):
    account.sell_shares(symbol, quantity)
    return f"Sold {quantity} shares of {symbol}. New balance: ${account.balance}"

def get_portfolio_value():
    return f"Total Portfolio Value: ${account.calculate_portfolio_value()}"

def get_profit_loss(initial_deposit):
    return f"Profit/Loss since initial deposit: ${account.calculate_profit_loss(initial_deposit)}"

def get_holdings():
    return account.report_holdings()

def get_transactions():
    return account.list_transactions()

# --- Gradio 4.x Interface using Blocks ---
with gr.Blocks(title="Simple Account Management System") as demo:
    gr.Markdown("## 💰 Simple Account Management System\nDemo trading simulation platform")

    # --- Account Creation Section ---
    with gr.Row():
        initial_balance = gr.Number(label="Initial Balance", value=1000)
        create_btn = gr.Button("Create Account")
        create_output = gr.Textbox(label="Result")
        create_btn.click(fn=create_account, inputs=initial_balance, outputs=create_output)

    # --- Deposit / Withdraw Section ---
    with gr.Row():
        deposit_amount = gr.Number(label="Deposit Amount")
        deposit_btn = gr.Button("Deposit Funds")
        deposit_output = gr.Textbox(label="Result")
        deposit_btn.click(fn=deposit_funds, inputs=deposit_amount, outputs=deposit_output)

    with gr.Row():
        withdraw_amount = gr.Number(label="Withdraw Amount")
        withdraw_btn = gr.Button("Withdraw Funds")
        withdraw_output = gr.Textbox(label="Result")
        withdraw_btn.click(fn=withdraw_funds, inputs=withdraw_amount, outputs=withdraw_output)

    # --- Buy / Sell Shares Section ---
    with gr.Row():
        buy_symbol = gr.Textbox(label="Stock Symbol")
        buy_quantity = gr.Number(label="Quantity")
        buy_btn = gr.Button("Buy Shares")
        buy_output = gr.Textbox(label="Result")
        buy_btn.click(fn=buy_shares, inputs=[buy_symbol, buy_quantity], outputs=buy_output)

    with gr.Row():
        sell_symbol = gr.Textbox(label="Stock Symbol")
        sell_quantity = gr.Number(label="Quantity")
        sell_btn = gr.Button("Sell Shares")
        sell_output = gr.Textbox(label="Result")
        sell_btn.click(fn=sell_shares, inputs=[sell_symbol, sell_quantity], outputs=sell_output)

    # --- Portfolio & Reports Section ---
    with gr.Row():
        value_btn = gr.Button("Get Portfolio Value")
        value_output = gr.Textbox(label="Portfolio Value")
        value_btn.click(fn=get_portfolio_value, outputs=value_output)

    with gr.Row():
        profit_input = gr.Number(label="Initial Deposit")
        profit_btn = gr.Button("Get Profit/Loss")
        profit_output = gr.Textbox(label="Profit/Loss")
        profit_btn.click(fn=get_profit_loss, inputs=profit_input, outputs=profit_output)

    with gr.Row():
        holdings_btn = gr.Button("View Holdings")
        holdings_output = gr.Textbox(label="Holdings")
        holdings_btn.click(fn=get_holdings, outputs=holdings_output)

    with gr.Row():
        transactions_btn = gr.Button("View Transactions")
        transactions_output = gr.Textbox(label="Transactions")
        transactions_btn.click(fn=get_transactions, outputs=transactions_output)

# --- Launch app ---
demo.launch(share=True)
