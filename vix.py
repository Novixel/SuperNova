# Start with a Stable Coin in portfolio e.i USDC USDT DAI

# Take all that stable and buy Bitcoin!

# Use the bitcoin to trade with another coin e.i ALGO ETH 

# we pic algo for this one

# take STABLE and convert to BTC

# take BTC and convert to ALGO

# accumulate +1 USDT of ALGO

# sell 1 usdt of Algo for BTC

# sell 1 usdt of btc to HOLD 1 extra 

from time import sleep

from tradingview_ta.technicals import Compute
import TVIndicators as TV
from data.items import AccountItem, ProductItem
from dataclasses import asdict
import envVars.tenv 

from data.connect import Connect
from data.manager import Manager
from data.user import User
from datetime import datetime

def main():
    user = User()
    con = Connect(user.name, user.api)
    man = Manager(con)
    # base, quote, product = man.check_Pair("BTC-USDT")
    # currentUSDT = quote.available
    # currentBTC = base.available
    # currentPrice = float(man.Client.get_product_ticker(product.id)['price'])
    # sizeConvert = ('%.8f'%((1/currentPrice*(currentUSDT-(currentUSDT*0.005)))))
    # print(f"sending trade {product.id}, 'buy', {currentPrice}, {sizeConvert}")
    # initTrade = man.Trade(product.id, "buy", currentPrice, sizeConvert)
    # currentUSDT = quote.available
    # currentBTC = sizeConvert
    # sleep(30)
    base, quote, product = man.check_Pair("ALGO-BTC")
    currentBTC = base.available
    currentALGO = quote.available
    currentPrice = float(man.Client.get_product_ticker(product.id)['price'])
    sizeConvert = ('%.8f'%((1/currentPrice*currentALGO)))
    firstTrade = man.Trade((product.id), "buy", currentPrice, 1)
    sleep(30)
    autoTrades = man.Auto_Trader(product.id, 60*12)
    print(f"{firstTrade = }")
    input('Continue?')
    for i in autoTrades:
        print(i)
    base, quote, product = man.check_Pair("BTC-USDT")
    currentUSDT = quote.available
    base, quote, product = man.check_Pair("ALGO-BTC")
    currentBTC = base.available
    currentALGO = quote.available
    print(f"{currentUSDT = }")
    print(f"{currentALGO = }")
    print(f"{currentBTC = }")
    input('Continue?')



if __name__ == "__main__":
    main()