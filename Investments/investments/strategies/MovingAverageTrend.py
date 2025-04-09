from matplotlib import pyplot as plt
from numpy.ma.extras import average


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
            tmp = self.prices[i - self.moving_average_1_period: i]
            self.moving_average_1.append(average(tmp))

        for i in range(self.moving_average_2_period, len(self.prices) + 1):
            tmp = self.prices[i - self.moving_average_2_period: i]
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

    def visualize(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12, 8))
        ax1.plot(range(len(self.prices)), self.prices, label="Price", color="blue", linestyle="-")
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
        ax2.set_ylabel("Trend (1: Bullish, -1: Bearish, 0: Neutral)")
        ax2.grid(True)

        plt.tight_layout()
        plt.show()


test = MovingAverage(9, 20, [
    172.42, 181.46, 188.38, 203.19, 223.89, 223.19, 222.13, 217.9, 223.85,
    221.53, 223.75, 220.73, 218.27, 214.1, 215.24, 212.69, 214.0, 213.49,
    209.68, 216.98, 220.84, 227.48, 239.07, 235.33, 235.74, 235.93, 238.03,
    241.84, 237.3, 240.36, 247.04, 247.1, 245.55, 245.83, 244.87, 244.47,
    244.6, 241.53, 236.87, 232.62, 227.65, 227.63, 233.22, 232.47, 232.8,
    228.01, 236.0, 237.59, 239.36, 238.26, 229.86, 222.78, 223.66, 223.83,
    222.64, 229.98, 228.26, 237.87, 233.28, 234.4, 236.85, 242.7, 242.21,
    245.0, 243.36, 243.85, 250.42, 252.2, 255.59, 259.02, 258.2, 255.27,
    254.49, 249.79, 248.05, 253.48, 251.04, 248.13, 247.96, 246.49, 247.77,
    246.75, 242.84, 243.04, 243.01, 242.65, 239.59, 237.33, 234.93, 235.06,
    232.87, 229.87, 228.52, 229.0, 228.28, 228.02, 225.0, 228.22, 225.12,
    224.23, 224.23, 226.96, 227.48, 222.72, 223.45, 222.01, 222.91, 225.91,
    230.1, 233.67, 233.4, 231.41, 230.57, 230.76, 235.86, 236.48, 235.0,
    232.15, 231.78, 233.85, 231.3, 227.55, 229.04, 229.54, 225.77, 221.69,
    226.8, 225.67, 226.78, 226.21, 233.0, 227.79, 227.52, 226.37, 227.37,
    226.47, 228.2, 228.87, 220.69, 216.79, 216.32, 222.5, 222.77, 222.66,
    220.11, 220.91, 220.82, 222.38, 220.85, 222.77, 229.0, 229.79, 226.49,
    228.03, 227.18, 226.84, 224.53, 226.4, 226.51, 225.89, 226.05, 224.72,
    221.72, 221.27, 217.53, 216.24, 213.31, 209.82, 207.23, 209.27, 219.86,
    218.36, 222.08, 218.8, 218.24, 217.96, 217.49, 218.54, 225.01, 223.96,
    224.31, 224.18, 228.88, 234.82, 234.4, 230.54, 227.57, 232.98, 228.68,
    227.82, 226.34, 221.55, 220.27, 216.75, 210.62, 214.1, 213.25, 209.07,
    208.14, 207.49, 209.68, 214.29, 216.67, 212.49, 214.24, 213.07, 207.15,
    193.12, 196.89, 194.48, 195.87, 194.35, 194.03, 192.25, 191.29, 190.29,
    189.99, 189.98, 186.88, 190.9, 192.35, 191.04, 189.87, 189.84, 189.72,
    187.43, 186.28, 183.05, 184.57, 182.74, 182.4, 181.71, 183.38, 173.03,
    169.3, 170.33, 173.5, 169.3, 169.89, 169.02, 166.9, 165.84, 165.0, 167.04,
    168.0, 169.38, 172.69, 176.55, 175.04, 167.78, 169.67, 168.45, 169.58,
    168.82, 169.65, 168.84, 170.03, 171.48, 173.31, 169.71, 170.85, 172.28,
    171.37, 178.67, 176.08, 173.72, 172.62, 173.0, 171.13, 173.23, 172.75,
    170.73, 169.0, 169.12, 170.12, 175.1, 179.66, 180.75, 181.42, 182.63,
    181.16, 182.52, 184.37, 182.32, 181.56, 182.31, 183.86, 184.15, 185.04,
    187.15, 188.85, 188.32, 189.41, 189.3, 187.68, 185.85, 186.86, 184.4,
    188.04, 191.73, 192.42, 194.17, 194.5, 195.18, 193.89, 191.56, 188.63,
    182.123
])
test.calculate_averages()
test.trend_initializer()
test.visualize()

print("Moving Average 1:", test.moving_average_1)
print("Moving Average 2:", test.moving_average_2)
print("Trend:", test.trend)
