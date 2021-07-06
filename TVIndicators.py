from tradingview_ta import TA_Handler, Interval, Exchange
from datetime import timedelta, datetime
from time import sleep

# product = TA_Handler(
#     symbol="BTCUSDC",
#     screener="crypto",
#     exchange="COINBASE",
#     interval=Interval.INTERVAL_15_MINUTES
# )
# indic = product.get_analysis().indicators

# for i,v in indic.items():
#     print(i,v)

class TradeIndicator():
    def __init__(self,symbol):
        self.product = TA_Handler(
            symbol=symbol,
            screener="crypto",
            exchange="COINBASE",
            interval=Interval.INTERVAL_15_MINUTES
        )
        self.update()

    def update(self):
        analysis = self.product.get_analysis()
        symbol = analysis.symbol
        exchange = analysis.exchange
        screener = analysis.screener
        self.interval = analysis.interval
        self.time = analysis.time
        self.summary = analysis.summary
        self.oscillators = analysis.oscillators
        self.moving_avgs = analysis.moving_averages
        self.indicators = analysis.indicators
        print("Updated at",self.time)
        
    def PrintAll(self):
        for i, v in self.indicators.items():
            print(i,v)
            self.i = v

    def Get(self,item):
        now = datetime.now()
        time = now - self.time
        time = time.total_seconds()
        mins = divmod(time, 60)[0]
        # print("Now:",now)
        # print("init:",self.time)
        # print(mins)
        if 2.0 <= mins:
            self.update()
            self.time = datetime.now()
        indic = self.indicators
        if item in indic:
            return float(indic[item])


if __name__=="__main__":
    indicator = TradeIndicator("BTCUSD")
    while True:
        print("Checking At:",indicator.time.strftime("%c"))
        print("OSCILLATORS:")
        for k,v in indicator.oscillators.items():
            print(k,"=",v)
        print("MOVING_AVGS:")
        for k,v in indicator.moving_avgs.items():
            print(k,"=",v)
        sleep(60)
        