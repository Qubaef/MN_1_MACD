import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as src


def ema(data, n):
    a = 2/(n + 1)
    ema = []

    # loop through rows, starting from n'th row
    for i in range(0, len(data)):
        if i >= n:
            licznik = 0
            mianownik = 0
            for j in range(i, i - n - 1, -1):
                licznik += data[j] * a ** (i - j)
                mianownik += a ** (i - j)
            ema.append(licznik/mianownik)
        else:
            ema.append(0)
    return ema


day_diff = 1000             # get 1000 units
end = dt.date(2020, 2, 1)
start = end - dt.timedelta(days = day_diff)

foldername = 'data'
column = 'Open'
symbol = 'AMD'
filename = symbol + '.csv'
data_source = 'yahoo'       # get stock data from 'Yahoo! Finance' acording to pandas_datareader docs

data = src.data.DataReader(symbol, data_source, start, end)[column]
data.to_csv(foldername + '/' + filename)
df = pd.read_csv(foldername + '/' + filename, header = 0, index_col = 'Date' , parse_dates = True)


macd = []
ema12 = ema(df[column], 12)
ema26 = ema(df[column], 26)

# macd = ema12 - ema26
for i in range(0, len(ema26)):
    macd.append(ema12[i] - ema26[i])

# signal = ema9(macd)
signal = ema(macd, 9)

#macd = [list(range(0,len(macd) - 1)), macd]
#signal = [list(range(14,len(signal) - 1)), signal]

#macdIndexed = []
#for i in range(0, len(macd)):
#    macdIndexed.append([i , macd[i]])

#signalIndexed = []
#for i in range(9, len(signal)):
#    signalIndexed.append([i , signal[i]])

plt.plot(df[column])
plt.show()

plt.plot(macd, 'b')
plt.plot(signal, 'r')
plt.show()


# 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14
# 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28
#                                           26 27 28
