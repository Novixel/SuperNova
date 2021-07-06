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

def CheckMarket(product_id):
    Tview = TV.TradeIndicator((product_id.replace("-","")))
    vote = Tview.moving_avgs["RECOMMENDATION"]
    print("RECOMMENDATION = ",vote)
    if vote == "STRONG_BUY":
        return "sell"
    elif vote == "STRONG_SELL":
        return "buy"
    else:
        return "wait"

def main():
    user = User()
    con = Connect(user.name, user.api)
    man = Manager(con)
    pros = man.Products
    selection = "BTC-USDC" #input('Enter a product i.e. BTC-USD :\n')
    for p in range(len(pros)):
        if selection == pros[p].id:
            product_id = pros[p].id
            break
    vote = CheckMarket(product_id)
    if vote != "wait":
        base, quote, product = man.check_Pair(product_id)
        debug = True
        if debug or base.available > product.base_min_size or quote.available > product.min_market_funds:
            current = man.Client.get_product_ticker(product_id)["price"]
            trade = man.fake_trade(product_id,vote,product.base_min_size,float(current))
            with open("trades.txt","a") as a:
                a.write(str(trade) + "\n")
                a.close
        else:
            print('Please Add More Funds To Your Account In Order To Start Trading!')
            exit()

if __name__ == "__main__":
    while True:
        main()
        sleep(10)