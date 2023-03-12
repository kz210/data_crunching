import yfinance as yf
import matplotlib.pyplot as plt


def retrieve_yahoo_data(ticks, start_date, end_date):
    data = yf.download(ticks, start_date, end_date)
    return data


def plot_sample():
    x = list(range(10))
    y = [2 * i for i in x]
    plt.scatter(x, y)
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ticks = "SPY AAPL"
    start_date = "2017-01-01"
    end_date = "2017-04-30"
    data = retrieve_yahoo_data(ticks, start_date, end_date)
    print(data.head())

