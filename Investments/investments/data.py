import pandas as pd
import yfinance as yf

def dane_daj():
    # Dane apple
    apple = pd.read_csv('./data/apple_10y.csv')
    apple['Close/Last'] = apple['Close/Last'].str.replace(r'\$', '', regex=True).astype(float)

    # BTC
    btc = yf.download("BTC-USD", start="2014-09-16", end="2025-05-08")

    # Nvidia
    nvidia = yf.download("NVDA", start="2014-09-16", end="2025-05-08")

    # XRP
    xrp = yf.download("XRP-USD", start="2014-09-16", end="2025-05-08")

    # Gold
    gold = yf.download("GC=F", start="2014-09-16", end="2025-05-08")

    # Silver
    silver = yf.download("SI=F", start="2014-09-16", end='2025-05-08')

    return apple, btc, nvidia, xrp, silver, gold

apple, btc, nvidia, xrp, silver, gold = dane_daj()
print(apple['Close/Last'].tolist())