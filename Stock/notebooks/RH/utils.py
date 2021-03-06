import pandas as pd
import backtrader as bt

def hello():
    pass

def read_ami_SPY_data():
    spy_data = pd.read_excel('SPY_1999_2017.xlsx')
    spy_data.rename(columns={'Date/Time':'Date', 'O': 'Open', 'H': 'High', 'L': 'Low', 'C': 'Close', 'V': 'Volume'}, inplace=True)
    spy_data.drop('Ticker', axis=1, inplace=True)
    spy_data.set_index('Date', inplace=True)
    
    spy_data.fillna(method='ffill', inplace=True)
    spy_data.fillna(method='bfill', inplace=True)
    return spy_data

def read_data(filename):
    data = pd.read_excel(filename, skiprows=1, index_col='Date')
    data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    data.dropna(inplace=True)
    return data

class BaseStrategy(bt.Strategy):
    
    def __init__(self):
        pass
    
    def next(self):
        pass
    
    def canceled(self):
        pass
    
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        
    def log_candles(self):
        self.log('===>')
        self.log('Current Open: {}, Close: {}'.format(self.data0.open[0],self.data0.close[0]))
        self.log('Next Open: {}, Close: {}'.format(self.data0.open[1],self.data0.close[1]))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
            self.canceled()