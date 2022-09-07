
import MetaTrader5 as mt5
import pandas as pd
import time

SYMBOL = 'BTCUSD'
TIMEFRAME = mt5.TIMEFRAME_M1
VOLUME = 1.0
DEVIATION = 20
MAGIC = 10
SMA_PERIOD = 20
STANDARD_DEVIATIONS = 2
TP_SD = 2
SL_SD = 3

def market_order(symbol, volume, order_type, deviation, magic, stoploss, takeprofit):
    tick = mt5.symbol_info_tick(symbol)

    order_dict = {'buy':0, 'sell':1}
    price_dict = {'buy':tick.ask, 'sell': tick.bid}

    request = {
        'action': mt5.TRADE_ACTION_DEAL,
        'symbol': symbol,
        'volume': volume,
        'type': order_dict[order_type],
        'price': price_dict[order_type],
        'deviation': deviation,
        'magic': magic,
        'sl':stoploss,
        'tp': takeprofit,
        'connect': 'python_market_order',
        'type_time': mt5.ORDER_TIME_GTC,
        'tyoe_filling': mt5.ORDER_FILLING_IOC,
    }
    order_result = mt5.order_send(request)
    print(order_result)

    return order_result

def get_signal():
    bars = mt5.copy_rates_from_pos(SYMBOL, TIMEFRAME, 1, SMA_PERIOD)

    df = pd.DataFrame(bars)
    sma = df['close'].mean()
    sd = df['close'].std()
    lower_band = sma - STANDARD_DEVIATIONS * sd
    upper_band = sma + STANDARD_DEVIATIONS * sd
    last_close_price = df.iloc[-1]['close']
    print(last_close_price, upper_band)

    if last_close_price < lower_band:
        return 'buy', sd
    elif last_close_price > upper_band:
        return 'sell', sd
    else:
        return [None, None]

initialized = mt5.initialize()

if initialized:
    print('connected to Metatrader5')
    print('Login: ', mt5.account_info().login)
    print('Server: ', mt5.account_info().server)

while True:
    # strategy logic
    # if no positions are open
    if mt5.positions_total() == 0:
        signal, standard_deviation = get_signal()
        print(signal, standard_deviation)

        tick = mt5.symbol_info_tick(SYMBOL)
        if signal == 'buy':
            market_order(SYMBOL, VOLUME, 'buy', 20, 10, tick.bid - SL_SD * standard_deviation,
                         tick.bid + TP_SD * standard_deviation)
        elif signal == 'sell':
            market_order(SYMBOL, VOLUME, 'sell', 20, 10, tick.bid + SL.SD * standard_deviation,
                         tick.bid - TP_SD * standard_deviation)
    time.sleep(1)















