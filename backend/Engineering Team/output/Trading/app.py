import gradio as gr
from accounts import Account, get_share_price
import pandas as pd

def _new_account(initial_balance):
    acc = Account(initial_balance)
    return acc, f"✅ Account created with initial balance: ${initial_balance:.2f}", acc.balance

def _deposit(acc, amount):
    try:
        acc.deposit_funds(amount)
        return acc, f"✅ Deposited ${float(amount):.2f}", acc.balance
    except Exception as e:
        return acc, f"❌ {e}", acc.balance

def _withdraw(acc, amount):
    try:
        acc.withdraw_funds(amount)
        return acc, f"✅ Withdrew ${float(amount):.2f}", acc.balance
    except Exception as e:
        return acc, f"❌ {e}", acc.balance

def _buy(acc, symbol, qty):
    try:
        acc.buy_shares(symbol, qty)
        return acc, f"✅ Bought {int(qty)} {str(symbol).upper()}", acc.balance
    except Exception as e:
        return acc, f"❌ {e}", acc.balance

def _sell(acc, symbol, qty):
    try:
        acc.sell_shares(symbol, qty)
        return acc, f"✅ Sold {int(qty)} {str(symbol).upper()}", acc.balance
    except Exception as e:
        return acc, f"❌ {e}", acc.balance

def _holdings_table(acc):
    holdings = acc.report_holdings()
    data = []
    for s, q in holdings.items():
        price = get_share_price(s)
        value = (price or 0) * q
        data.append([s, q, price, round(value, 2)])
    return data

def _transactions_table(acc):
    txs = acc.list_transactions()
    if not txs:
        return []
    df = pd.DataFrame(txs)
    return df

def _portfolio_value(acc):
    return f"${acc.calculate_portfolio_value():.2f}"

def _profit_loss(acc, initial_deposit):
    try:
        return f"${acc.calculate_profit_loss(initial_deposit):.2f}"
    except Exception as e:
        return f"❌ {e}"

with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo", neutral_hue="slate"),
               title="Simple Account Management System") as demo:

    gr.Markdown("# 💹 Trading Simulator\nModern tabbed demo for funds, trading, and reports.")

    acc_state = gr.State(Account(1000))

    with gr.Tabs():
        with gr.TabItem("🏦 Account"):
            init_bal = gr.Number(label="Initial Balance", value=1000.00)
            create_btn = gr.Button("Create Account", variant="primary")
            create_msg = gr.Textbox(label="Status", interactive=False)
            live_balance = gr.Number(label="Current Balance", value=1000.00, interactive=False)
            create_btn.click(_new_account, inputs=init_bal, outputs=[acc_state, create_msg, live_balance])

        with gr.TabItem("💵 Funds"):
            gr.Markdown("### Deposit")
            deposit_amt = gr.Number(label="Amount", value=100)
            deposit_btn = gr.Button("Deposit", variant="primary")
            deposit_msg = gr.Textbox(label="Status", interactive=False)
            deposit_btn.click(_deposit, inputs=[acc_state, deposit_amt], outputs=[acc_state, deposit_msg, live_balance])

            gr.Markdown("### Withdraw")
            withdraw_amt = gr.Number(label="Amount", value=50)
            withdraw_btn = gr.Button("Withdraw")
            withdraw_msg = gr.Textbox(label="Status", interactive=False)
            withdraw_btn.click(_withdraw, inputs=[acc_state, withdraw_amt], outputs=[acc_state, withdraw_msg, live_balance])

        with gr.TabItem("📈 Trading"):
            buy_symbol = gr.Textbox(label="Buy Symbol", placeholder="AAPL")
            buy_qty = gr.Number(label="Quantity", value=1, precision=0)
            buy_btn = gr.Button("Buy", variant="primary")
            buy_msg = gr.Textbox(label="Status", interactive=False)
            buy_btn.click(_buy, inputs=[acc_state, buy_symbol, buy_qty], outputs=[acc_state, buy_msg, live_balance])

            sell_symbol = gr.Textbox(label="Sell Symbol", placeholder="AAPL")
            sell_qty = gr.Number(label="Quantity", value=1, precision=0)
            sell_btn = gr.Button("Sell")
            sell_msg = gr.Textbox(label="Status", interactive=False)
            sell_btn.click(_sell, inputs=[acc_state, sell_symbol, sell_qty], outputs=[acc_state, sell_msg, live_balance])

            gr.Markdown("### Holdings")
            holdings = gr.Dataframe(
                headers=["Symbol", "Quantity", "Price", "Market Value"],
                interactive=False
            )
            refresh_holdings = gr.Button("Refresh Holdings")
            refresh_holdings.click(_holdings_table, inputs=acc_state, outputs=holdings)

        with gr.TabItem("📊 Reports"):
            pv_btn = gr.Button("Calculate Portfolio Value", variant="primary")
            pv_out = gr.Textbox(label="Portfolio Value", interactive=False)
            pv_btn.click(_portfolio_value, inputs=acc_state, outputs=pv_out)

            init_dep = gr.Number(label="Initial Deposit (for P/L)", value=1000.00)
            pl_btn = gr.Button("Calculate Profit/Loss")
            pl_out = gr.Textbox(label="Profit/Loss", interactive=False)
            pl_btn.click(_profit_loss, inputs=[acc_state, init_dep], outputs=pl_out)

            gr.Markdown("### Transactions")
            tx_df = gr.Dataframe(headers=["ts","type","symbol","qty","price","amount","note","balance"], interactive=False)
            refresh_tx = gr.Button("Refresh Transactions")
            refresh_tx.click(_transactions_table, inputs=acc_state, outputs=tx_df)

demo.queue().launch(share=True)
