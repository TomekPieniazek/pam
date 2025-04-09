import io
from flask import Flask, request, send_file, abort
import pandas as pd
import yfinance as yf
from numpy.ma.extras import average
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def dane_daj():
    apple = pd.read_csv('./data/apple_10y.csv')
    apple['Close/Last'] = apple['Close/Last'].str.replace(r'\$', '', regex=True).astype(float)
    btc = yf.download("BTC-USD", start="2014-09-16", end="2025-05-08")
    nvidia = yf.download("NVDA", start="2014-09-16", end="2025-05-08")
    xrp = yf.download("XRP-USD", start="2014-09-16", end="2025-05-08")
    gold = yf.download("GC=F", start="2014-09-16", end="2025-05-08")
    silver = yf.download("SI=F", start="2014-09-16", end="2025-05-08")
    return apple, btc, nvidia, xrp, silver, gold

apple, btc, nvidia, xrp, silver, gold = dane_daj()

DATA_MAP = {
    'apple': ('Close/Last', apple),
    'btc': ('Close', btc),
    'nvidia': ('Close', nvidia),
    'xrp': ('Close', xrp),
    'silver': ('Close', silver),
    'gold': ('Close', gold)
}

class MovingAverage():
    def __init__(self, moving_average_1, moving_average_2, data):
        self.locked = False
        self.transactions = []
        self.moving_average_1_period = moving_average_1
        self.moving_average_2_period = moving_average_2
        self.trend = []
        self.prices = data
        self.moving_average_1 = []
        self.moving_average_2 = []

    def check_is_locked(self):
        return self.locked

    def calculate_averages(self):
        for i in range(self.moving_average_1_period, len(self.prices) + 1):
            tmp = self.prices[i - self.moving_average_1_period:i]
            self.moving_average_1.append(average(tmp))
        for i in range(self.moving_average_2_period, len(self.prices) + 1):
            tmp = self.prices[i - self.moving_average_2_period:i]
            self.moving_average_2.append(average(tmp))

    def trend_initializer(self):
        offset = self.moving_average_2_period - self.moving_average_1_period
        for i in range(len(self.moving_average_2)):
            short_ma = self.moving_average_1[i + offset]
            long_ma = self.moving_average_2[i]
            if short_ma > long_ma:
                self.trend.append(1)
            elif short_ma < long_ma:
                self.trend.append(-1)
            else:
                self.trend.append(0)

    def open(self):
        self.locked = True

    def close(self):
        self.locked = False

    def plot_to_png(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12, 8))
        ax1.plot(range(len(self.prices)), self.prices, label="Price", color="blue")
        x1 = list(range(self.moving_average_1_period - 1, len(self.prices)))
        x2 = list(range(self.moving_average_2_period - 1, len(self.prices)))
        ax1.plot(x1, self.moving_average_1, label=f"MA {self.moving_average_1_period}", color="orange")
        ax1.plot(x2, self.moving_average_2, label=f"MA {self.moving_average_2_period}", color="green")
        ax1.set_title("Price and Moving Averages")
        ax1.set_ylabel("Price")
        ax1.grid(True)
        ax1.legend()
        trend_x = list(range(self.moving_average_2_period - 1, self.moving_average_2_period - 1 + len(self.trend)))
        ax2.stem(trend_x, self.trend, basefmt=" ")
        ax2.set_title("Trend")
        ax2.set_xlabel("Time Index")
        ax2.set_ylabel("Trend (1 = Bullish, -1 = Bearish, 0 = Neutral)")
        ax2.grid(True)
        plt.tight_layout()
        canvas = FigureCanvas(fig)
        buf = io.BytesIO()
        canvas.print_png(buf)
        buf.seek(0)
        plt.close(fig)
        return buf

app = Flask(__name__)

@app.route('/api/plot')
def plot_stock():
    stock = request.args.get('stock', '').lower()
    if stock not in DATA_MAP:
        return abort(404, description=f"Stock '{stock}' not found. Valid options: {list(DATA_MAP.keys())}")
    col_name, df = DATA_MAP[stock]
    try:
        prices = df[col_name].tolist()
    except Exception as e:
        return abort(500, description=f"Error processing data for {stock}: {str(e)}")
    ma = MovingAverage(50, 200, prices)
    ma.calculate_averages()
    ma.trend_initializer()
    png_image = ma.plot_to_png()
    return send_file(png_image, mimetype='image/png', as_attachment=False)

@app.route('/api/info')
def info():
    return {
        "available_stocks": list(DATA_MAP.keys()),
        "message": "Use /api/plot?stock=<stock_symbol> to get a moving averages plot."
    }

if __name__ == '__main__':
    app.run(debug=True)
