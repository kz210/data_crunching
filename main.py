# from __future__ import (absolute_import, division, print_function,
#                         unicode_literals)
#
# from datetime import datetime  # For datetime objects
# import yfinance as yf
# import os.path  # To manage paths
# import sys  # To find out the script name (in argv[0])
#
#
# # Import the backtrader platform
# import backtrader as bt
#
#
# # Create a Stratey
# class TestStrategy(bt.Strategy):
#     params = (
#         ('maperiod', 15),
#         ('printlog', False),
#     )
#
#     def log(self, txt, dt=None, doprint=False):
#         ''' Logging function fot this strategy'''
#         if self.params.printlog or doprint:
#             dt = dt or self.datas[0].datetime.date(0)
#             print('%s, %s' % (dt.isoformat(), txt))
#
#     def __init__(self):
#         # Keep a reference to the "close" line in the data[0] dataseries
#         self.dataclose = self.datas[0].close
#
#         # To keep track of pending orders and buy price/commission
#         self.order = None
#         self.buyprice = None
#         self.buycomm = None
#
#         # Add a MovingAverageSimple indicator
#         self.sma = bt.indicators.SimpleMovingAverage(
#             self.datas[0], period=self.params.maperiod)
#
#     def notify_order(self, order):
#         if order.status in [order.Submitted, order.Accepted]:
#             # Buy/Sell order submitted/accepted to/by broker - Nothing to do
#             return
#
#         # Check if an order has been completed
#         # Attention: broker could reject order if not enough cash
#         if order.status in [order.Completed]:
#             if order.isbuy():
#                 self.log(
#                     'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
#                     (order.executed.price,
#                      order.executed.value,
#                      order.executed.comm))
#
#                 self.buyprice = order.executed.price
#                 self.buycomm = order.executed.comm
#             else:  # Sell
#                 self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
#                          (order.executed.price,
#                           order.executed.value,
#                           order.executed.comm))
#
#             self.bar_executed = len(self)
#
#         elif order.status in [order.Canceled, order.Margin, order.Rejected]:
#             self.log('Order Canceled/Margin/Rejected')
#
#         # Write down: no pending order
#         self.order = None
#
#     def notify_trade(self, trade):
#         if not trade.isclosed:
#             return
#
#         self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
#                  (trade.pnl, trade.pnlcomm))
#
#     def next(self):
#         # Simply log the closing price of the series from the reference
#         self.log('Close, %.2f' % self.dataclose[0])
#
#         # Check if an order is pending ... if yes, we cannot send a 2nd one
#         if self.order:
#             return
#
#         # Check if we are in the market
#         if not self.position:
#
#             # Not yet ... we MIGHT BUY if ...
#             if self.dataclose[0] > self.sma[0]:
#
#                 # BUY, BUY, BUY!!! (with all possible default parameters)
#                 self.log('BUY CREATE, %.2f' % self.dataclose[0])
#
#                 # Keep track of the created order to avoid a 2nd order
#                 self.order = self.buy()
#
#         else:
#
#             if self.dataclose[0] < self.sma[0]:
#                 # SELL, SELL, SELL!!! (with all possible default parameters)
#                 self.log('SELL CREATE, %.2f' % self.dataclose[0])
#
#                 # Keep track of the created order to avoid a 2nd order
#                 self.order = self.sell()
#
#     def stop(self):
#         self.log('(MA Period %2d) Ending Value %.2f' %
#                  (self.params.maperiod, self.broker.getvalue()), doprint=True)
#
#
# if __name__ == '__main__':
#     # Create a cerebro entity
#     cerebro = bt.Cerebro()
#
#     # Add a strategy
#     strats = cerebro.optstrategy(
#         TestStrategy,
#         maperiod=range(10, 31))
#
#     # Datas are in a subfolder of the samples. Need to find where the script is
#     # because it could have been called from anywhere
#     start_date, end_date = "2017-01-01", "2017-12-30"
#     tick = 'SPY'
#     df = yf.download(tick, start_date, end_date)
#     df['openinterest'] = 0
#     df.rename(columns = {'Date':'datetime','Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume'},
#               inplace= True)
#     #df.set_index('datetime',inplace=True)
#     brf_daily = bt.feeds.PandasData(dataname =df, fromdate=datetime.strptime(start_date,'%Y-%m-%d'), todate=datetime.strptime(end_date,'%Y-%m-%d'))
#
#
#     #2.2 add data feed to cerebro
#     cerebro.adddata(brf_daily)
#
#
#     # Set our desired cash start
#     cerebro.broker.setcash(1000000.0)
#
#     # Add a FixedSize sizer according to the stake
#     cerebro.addsizer(bt.sizers.FixedSize, stake=10)
#
#     # Set the commission
#     cerebro.broker.setcommission(commission=0.0)
#
#     # Run over everything
#     cerebro.run(maxcpus=1)


# numbers = [2, 1, 0, 1, 2, 9, 1, 0]# [12, 6, 18, 10, 1, 0]#[3, 19, 191, 91, 3]#[2, 2, 3, 5, 4, 0]#
# def find_max_sum_pairing(nums):
#     dp = [0]*len(nums)
#     dp[0] = nums[0]
#     dp[1] = int(str(nums[0]) + str(nums[1]))
#
#     for i in range(2, len(nums)):
#         dp[i] = max(dp[i-2]+ int(str(nums[i-1]) + str(nums[i])), dp[i-1] + nums[i])
#     return dp[-1]
#
#
# print(find_max_sum_pairing(numbers))

#Ret:a boolean whether array can be split into paris of same elements
# def solution(A):
#     if len(A)%2 !=0:
#         return False
#     count_dict = dict()
#     for item in A:
#         count_dict[item] = count_dict.get(item, 0) + 1
#
#     for key, val in count_dict.items():
#         if val % 2 != 0:
#             return False
#     return True
#
# nums = [-1,-1,-2,-2,3,3,3,3]
# print(solution(nums))

# def solve(S):
#     from collections import defaultdict
#     max_distance = -1
#     digrams = defaultdict(list)
#     for i in range(len(S) - 1):
#         digram = S[i:i + 2]
#         digrams[digram].append(i)
#         if len(digrams[digram]) > 1:
#             distance = digrams[digram][-1] - digrams[digram][0]
#             max_distance = max(max_distance, distance)
#             # if distance > max_distance:
#             #     max_distance = distance
#     return max_distance
#
# if __name__ == '__main__':
#     assert 1 == solve("aaa")
#     assert 7 == solve("aakmaakmakda")
#     assert -1 == solve("codility")

from collections import defaultdict


class Graph():
    def __init__(self, vertices):
        self.graph = defaultdict(list)
        self.V = vertices

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def isCyclicUtil(self, v, visited, recStack):

        # Mark current node as visited and
        # adds to recursion stack
        visited[v] = True
        recStack[v] = True

        # Recur for all neighbours
        # if any neighbour is visited and in
        # recStack then graph is cyclic
        for neighbour in self.graph[v]:
            if visited[neighbour] == False:
                if self.isCyclicUtil(neighbour, visited, recStack) == True:
                    return True
            elif recStack[neighbour] == True:
                return True

        # The node needs to be popped from
        # recursion stack before function ends
        recStack[v] = False
        return False

    # Returns true if graph is cyclic else false
    def isCyclic(self):
        visited = [False] * (self.V + 1)
        recStack = [False] * (self.V + 1)
        for node in range(self.V):
            if visited[node] == False:
                if self.isCyclicUtil(node, visited, recStack) == True:
                    return True
        return False


# Driver code
if __name__ == '__main__':
    g = Graph(4)
    g.addEdge(0, 1)
    g.addEdge(0, 2)
    g.addEdge(1, 2)
    g.addEdge(2, 0)
    g.addEdge(2, 3)
    g.addEdge(3, 3)

    if g.isCyclic() == 1:
        print("Graph contains cycle")
    else:
        print("Graph doesn't contain cycle")