import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as src

def ema_generate(data, n):
    a = 2/(n + 1)
    ema = []

    # loop through rows, starting from n'th row
    for i in range(n, len(data)):
        numerator = 0
        denominator = 0
        for j in range(i, i - n - 1, -1):
            numerator += data[j] * a ** (i - j)
            denominator += a ** (i - j)
        ema.append(numerator/denominator)
    return ema


def macd_generate(data):
    macd = []
    ema12 = ema_generate(data, 12)
    ema26 = ema_generate(data, 26)

    # macd = ema12 - ema26
    for i in range(0, len(ema26)):
        macd.append(ema12[i + 14] - ema26[i])

    return macd


def signal_generate(macd):
    # signal = ema9(macd)
    return ema_generate(macd, 9)


day_diff = 2000             # get 1000 units
end = dt.date(2020, 2, 1)
start = end - dt.timedelta(days = day_diff)

foldername = 'data'
column = 'Adj Close'
symbol = 'INTC'
filename = symbol + '.csv'
data_source = 'yahoo'       # get stock data from 'Yahoo! Finance' acording to pandas_datareader docs

data = src.data.DataReader(symbol, data_source, start, end)[column]
data.to_csv(foldername + '/' + filename)
df = pd.read_csv(foldername + '/' + filename, header = 0, index_col = 'Date' , parse_dates = True).tail(1000)

macd = macd_generate(df[column])

original = []
for i in range(0, len(df[column])):
    original.append(df[column][i])

plt.plot(original, 'b')
plt.plot(macd, 'b')
plt.plot(signal_generate(macd), 'r')
plt.show()
