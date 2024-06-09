from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from datetime import datetime
import backtrader as bt
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


class MyStrategy(bt.Strategy):
    params = (
        ('exitbars', 5),
        ('maperiod', 15),
        ('printlog', False)
    )

    def log(self, txt, dt=None, doprint = False):
        ''' Logging function for this strategy'''
        ''' Logging function fot this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        # add indicator
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0],  period=self.params.maperiod)
        # keep track of pending orders
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Indicators for the plotting show
        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
        #                                     subplot=True)
        # bt.indicators.StochasticSlow(self.datas[0])
        # bt.indicators.MACDHisto(self.datas[0])
        # rsi = bt.indicators.RSI(self.datas[0])
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # bt.indicators.ATR(self.datas[0], plot=False)


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # check if an order is pending. if yes, we cannot send a 2nd one
        if self.order:
            return

        # check if we're in market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.dataclose[0] < self.sma[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)


if __name__=='__main__':
    #1. Create a cerebro
    cerebro = bt.Cerebro()

    #2. Add data feed
    #2.1 create data feed
    start_date, end_date = "2017-01-01", "2017-06-30"
    tick = 'SPY'
    df = yf.download(tick, start_date, end_date)
    df['openinterest'] = 0
    df.rename(columns = {'Date':'datetime','Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume'},
              inplace= True)
    #df.set_index('datetime',inplace=True)
    brf_daily = bt.feeds.PandasData(dataname =df, fromdate=datetime.strptime(start_date,'%Y-%m-%d'), todate=datetime.strptime(end_date,'%Y-%m-%d'))


    #2.2 add data feed to cerebro
    cerebro.adddata(brf_daily)

    #3. Add strategy
    strats = cerebro.optstrategy(
        MyStrategy,
        maperiod=range(10, 31))

    # add cash and commission
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)
    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    #print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    #4. Run
    cerebro.run(maxcpus=1)

    #5. Analysis
   # print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    #cerebro.plot()

