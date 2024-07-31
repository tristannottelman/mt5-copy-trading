import MetaTrader5 as mt5
import time
import os
import json

# Clear screen and set title
os.system('cls')
os.system('title CopyTrading')

# Account credentials
file_path = "accounts.json"
default_data = {
    "account_1": {
        "login": 0,
        "password": "password",
        "server": "server"
    },
    "account_2": {
        "login": 0,
        "password": "password",
        "server": "server"
    }
}

if not os.path.exists(file_path):
    with open(file_path, 'w') as json_file:
        json.dump(default_data, json_file, indent=4)
    print(f"{file_path} created.\n\nNow fill in the account credentials!")
    exit()
else:
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    print(f"Data loaded from {file_path}")

account_1 = data["account_1"]
account_2 = data["account_2"]

# Login to MetaTrader 5 account
def login_to_mt5_account(account):
    if not mt5.initialize():
        print(f"initialize() failed, error code: {mt5.last_error()}")
        return False
    if not mt5.login(account['login'], account['password'], account['server']):
        print(f"Failed to connect to account {account['login']}")
        return False
    print(f"Connected to account {account['login']}")
    return True

# Monitor trades on first account
def monitor_trades(account_1, account_2):
    # Login to the first account
    if not login_to_mt5_account(account_1):
        return

    # Get initial trades and store their IDs
    initial_trades_account_1 = mt5.positions_get()
    initial_trade_ids_account_1 = {trade.ticket for trade in initial_trades_account_1}

    # Dictionary to keep track of copied trades (account 1 ID -> account 2 ID)
    copied_trades = {}

    while True:
        # Get current trades
        current_trades_account_1 = mt5.positions_get()
        current_trade_ids_account_1 = {trade.ticket for trade in current_trades_account_1}

        # Determine new trades by removing initial trades from the current trades
        new_trade_ids = current_trade_ids_account_1 - initial_trade_ids_account_1

        # Iterate through new trades and check conditions
        for trade_id in new_trade_ids:
            trade = next((trade for trade in current_trades_account_1 if trade.ticket == trade_id), None)
            if trade:
                if trade_id not in copied_trades and trade.sl != 0 and trade.tp != 0:
                    if not login_to_mt5_account(account_2):
                        return
                    copied_trade_id = copy_trade_to_account_2(trade)
                    if copied_trade_id:
                        copied_trades[trade_id] = copied_trade_id
                    if not login_to_mt5_account(account_1):
                        return

        # Check for closed trades on account 1
        closed_trade_ids = set(copied_trades.keys()) - current_trade_ids_account_1

        # Iterate through copied trades to check if any trade has been closed on account 1
        for trade_id in closed_trade_ids:
            if not login_to_mt5_account(account_2):
                return
            result = close_trade_on_account_2(copied_trades[trade_id])
            if result != None:
                del copied_trades[trade_id]
            if not login_to_mt5_account(account_1):
                return

        time.sleep(1)

# Copy trade to second account
def copy_trade_to_account_2(trade):
    symbol = trade.symbol
    volume = trade.volume
    order_type = mt5.ORDER_TYPE_BUY if trade.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_SELL
    price = trade.price_current
    sl = trade.sl
    tp = trade.tp

    request = {
        'action': mt5.TRADE_ACTION_DEAL,
        'symbol': symbol,
        'volume': volume,
        'type': order_type,
        'price': price,
        'sl': sl,
        'tp': tp,
        'deviation': 20,
        'magic': 0,
        'comment': 'Copied trade',
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Failed to copy trade to account 2: {result.comment}")
        return None
    else:
        print(f"Trade copied to account 2 successfully with ticket {result.order}")
        return result.order

# Close trade on second account
def close_trade_on_account_2(trade_id):
    positions = mt5.positions_get()
    if positions is None:
        print(f"Failed to get positions for account 2: {mt5.last_error()}")
        return None

    for position in positions:
        if position.ticket == trade_id:
            symbol = position.symbol
            volume = position.volume
            order_type = mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY

            # Get the current market price for closing the position
            price = mt5.symbol_info_tick(symbol).bid if order_type == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(symbol).ask

            request = {
                'action': mt5.TRADE_ACTION_DEAL,
                'position': position.ticket,
                'symbol': symbol,
                'volume': volume,
                'type': order_type,
                'price': price,
                'deviation': 20,
                'magic': 0,
                'comment': 'Close copied trade',
                'type_time': mt5.ORDER_TIME_GTC,
                'type_filling': mt5.ORDER_FILLING_IOC,
            }

            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print(f"Failed to close trade on account 2: {result.comment}")
                return None
            else:
                print(f"Trade {trade_id} closed on account 2 successfully")
                return result.order

    print(f"Trade {trade_id} not found on account 2")
    return None

if __name__ == "__main__":
    monitor_trades(account_1, account_2)
