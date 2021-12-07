from telethon import TelegramClient, events, sync
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5
import substring


#TELEGRAMI CREDENTIALS
api_id = 8784760
api_hash = 'c6b1db80accefe2574779d843d0d55b8'
client = TelegramClient('session', api_id, api_hash)

#FTMO METATRADER LOGIN CREDENTIALS
mt5.initialize(
   login=1056003464,             
   password="6JR8DND4ZF",      
   server="FTMO-Server")

#ACCOUNT EQUITY
equity = 40000
 
# connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
else:
    print("Bot in ascolto..")



def open_trade(action, symbol, sl_points, tp_points, price):

    # prepare the buy request structure
    symbol_info = mt5.symbol_info(symbol)
    trade_type=""

    point = mt5.symbol_info(symbol).point

    tick_value = mt5.symbol_info(symbol).trade_tick_value
    tick_size = mt5.symbol_info(symbol).trade_tick_size

    pipValue = (tick_value * point) / tick_size

    if action == 'buy':
        current_price = mt5.symbol_info_tick(symbol).ask
        
        if(price < current_price):
            trade_type = mt5.ORDER_TYPE_BUY_LIMIT
        else:
            trade_type = mt5.ORDER_TYPE_BUY_STOP
        
        sl = price - sl_points * point
        tp = price + tp_points * point
        
    elif action =='sell':
        current_price = mt5.symbol_info_tick(symbol).bid

        if(price > current_price):
            trade_type = mt5.ORDER_TYPE_SELL_LIMIT
        else:
            trade_type = mt5.ORDER_TYPE_SELL_STOP
            
        sl = price + sl_points * point
        tp = price - tp_points * point
        
    
    lot = (equity / (pipValue * sl_points))
    lot = lot / 100
    lot = round(lot, 2)
    sl = round(sl, 4)
    buy_request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": lot,
        "type": trade_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "comment": "sent by python",
        "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
        "type_filling": mt5.ORDER_FILLING_FOK,
    }
    # send a trading request
    result = mt5.order_send(buy_request)
    print(result)
    return result, buy_request 



#ON CHANNEL NEW MESSAGE
@client.on(events.NewMessage(chats="provone96"))
async def my_event_handler(event):
    message = event.text
    if "FREE SIGNAL" in message:
        if "SELL" in message or "BUY" in message:
            list_tmp = message.splitlines()

            list_final = []
            for item in list_tmp:
                list_final.extend(item.split())
            list_final.remove("FREE")
            list_final.remove("SIGNAL:")
            list_final.remove("@")

            action = str(list_final[0].lower())
            symbol = str(list_final[1])
            price = float(list_final[2])

            multiplier = 100000
            if "JPY" in symbol:
                multiplier = 1000

            take_profit = float(list_final[6])
            tp = 0.0

            if take_profit > price:
                tp = (take_profit - price) * multiplier
            else:
                tp = (price - take_profit) * multiplier
            sl = tp / 3

            open_trade(action,symbol,sl,tp,price)

client.start()
client.run_until_disconnected()










