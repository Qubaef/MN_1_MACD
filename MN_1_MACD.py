import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as src

def ema_generate(data, n):
    a = 1 - 2/(n + 1)
    ema = []

    # loop through rows, starting from n'th row
    for i in range(n, len(data)):
        numerator = 0
        denominator = 0
        for j in range(i, i - n - 1, -1):
            numerator += data[j] * (a ** (i - j))
            denominator += (a ** (i - j))
        ema.append(numerator/denominator)
    return ema


def macd_generate(data):
    macd = []
    ema12 = ema_generate(data, 12)
    ema26 = ema_generate(data, 26)

    # macd = ema12 - ema26
    ema12 = ema12[14:]
    for i in range(0, len(ema26)):
        macd.append(ema12[i] - ema26[i])

    return macd


def signal_generate(macd):
    # signal = ema9(macd)
    return ema_generate(macd, 9)


day_diff = 2000             # get data from 2000 days
end = dt.date(2020, 2, 1)
start = end - dt.timedelta(days = day_diff)

length = 1000               # number of rows taken from downloaded data
foldername = 'data'
column = 'Open'             # name of the column, from which data is imported
symbol = 'INTC'             # symbol of company whose data is downloaded
filename = symbol + '.csv'
data_source = 'yahoo'       # get stock data from 'Yahoo! Finance' acording to pandas_datareader docs

data = src.data.DataReader(symbol, data_source, start, end)[column]
data.to_csv(foldername + '/' + filename)
df = pd.read_csv(foldername + '/' + filename, header = 0, index_col = 'Date' , parse_dates = True).tail(length)


#### calculate data
# calculate macd
macd = macd_generate(df[column])
# calculate signal from macd
signal = signal_generate(macd)
# get array with 'column' data
original = df[column].tolist()

# calculate x axis to position figures properly
x_axis = list(range(1,len(original) + 1))
plt.plot(x_axis, original, 'g', label=column)

#cut x_axis to move figures to the right
x_axis = x_axis[26:]

plt.plot(x_axis, macd, 'b', label="MACD")

#cut x_axis to move figures to the right
x_axis = x_axis[9:]
plt.plot(x_axis, signal, 'r', label="SIGNAL")

plt.legend()
plt.show()



