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


day_diff = 365*20             # get data from 2000 days
end = dt.date(2020, 2, 1)
start = end - dt.timedelta(days = day_diff)

length = 365*20               # number of rows taken from downloaded data
foldername = 'data'
column = 'Open'                 # name of the column, from which data is imported
# symbol = ['F', 'AAPL', 'AMD', 'INTC', 'BAC', 'MSFT', 'NOK', 'UBER', 'AAL', 'GE', 'JD', 'FB', 'TWTR']                  # symbol of company whose data is downloaded
symbol = ['FB']                  # symbol of company whose data is downloaded
data_source = 'yahoo'           # get stock data from 'Yahoo! Finance' acording to pandas_datareader docs
balances = []

for x in range(0, len(symbol)):
    filename = symbol[x] + '.csv'

    data = src.data.DataReader(symbol[x], data_source, start, end)[column]
    data.to_csv(foldername + '/' + filename)
    df = pd.read_csv(foldername + '/' + filename, header = 0, index_col = 'Date' , parse_dates = True).tail(length)


    #### calculate data
    # calculate macd
    macd = macd_generate(df[column])
    # calculate signal from macd
    signal = signal_generate(macd)
    macd = macd[9:]
    # get array with 'column' data
    original = df[column].tolist()
    original = original[35:]

    plt.plot(original, 'g', label=column)
    plt.plot(macd, 'b', label="MACD")
    plt.plot(signal, 'r', label="SIGNAL")
    
    plt.legend()
    plt.show()

    # cout profit from actions
    balance = 1000
    shares = 0

    if macd[0] > signal[0]:
        state = 1       # state=1 stands for 'over'
    else:
        state = 0       # state=0 stands for 'under'

    for i in range(0, len(original)):
        if(state == 1 and macd[i] < signal[i]):
            # sell shares
            balance += shares * original[i]
            shares = 0
            state = 0
        elif state == 0 and macd[i] > signal[i]:
            # buy shares
            shares = int(balance/original[i])
            balance -= original[i] * shares
            state = 1
    print('\nCompany: ' + symbol[x])
    print('Balance: ' + str(balance) + '\nShares: ' + str(shares))
    balance += shares * original[i]
    print('Balance for last day ' + str(balance))
    balances.append(balance)

for i in range(0, len(balances)):
    balance = balances[i] - 1000

print('Total profit ' + str(balance))
