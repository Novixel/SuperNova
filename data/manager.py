# Coinbase Pro Account Manager
# Codename: Algorand
# Author: Tristan "Novixel"
# v0.10
# manager.py

from data.items import AccountItem , ProductItem
import time
from datetime import datetime

class Manager():
    
    '''Everything Must Flow Threw The Manager!'''

    Accounts : list = []
    AvailableAccounts : list = []

    Products : list = []
    ProductPairs : list = []
    ProductMins : list = []

    totals: list = []
    Total: float = 0.0

    def __init__(self, connect, *special:bool):
        '''Connection Object, opt: True  = auto getTotals'''
        self.Connection = connect
        self.User = self.Connection.name
        self.Client = self.Connection.client()
        self.__getAccounts()
        self.__getProducts()
        if special:
            self.getTotal(start=True)
    
    def __getAccounts(self):
        Acc = self.Client.get_accounts()
        self.Accounts.clear()
        for a in Acc:
            self.Accounts.append(AccountItem(a))
            self.Currencys = a["currency"]
            if float(a["available"]) > 0:
                self.AvailableAccounts.append([a["currency"],a["available"]])

    def __getProducts(self):
        pros = self.Client.get_products()
        for a in pros:
            self.Products.append(ProductItem(a))
            self.ProductPairs.append(a["id"])
            self.ProductMins.append([a["id"], a["base_min_size"]])

    def getTotal(self,start:bool = False):
        print("\n...Getting.Total.BTC...\n...\n...Please.Wait...\n")
        self.totals.clear()
        if start:
            # if init started it we dont need to update accounts again
            pass
        else:
            print("getAccounts called from getTotal")
            self.__getAccounts()
        for i in self.Accounts:
            if (i.currency+"-BTC") in self.ProductPairs:
                t = float(self.Client.get_product_ticker((i.currency+"-BTC"))["price"]) # woop
                self.totals.append(float(float(i.available) * t))
                # print(i.currency+"-BTC""=","%.8f"%(float(i.available) * t))
            elif ("BTC-"+i.currency) in self.ProductPairs:
                t = float(self.Client.get_product_ticker(("BTC-"+i.currency))["price"]) # woop
                t = 1 / t
                self.totals.append(float(float(i.available) * t))
                # print("BTC-"+i.currency,"=","%.8f"%(float(i.available) * t))
            elif i.currency == "BTC":
                t = float(i.available)
                self.totals.append(t)
                # print("BTC = ","%.8f"%t)
            else:
                t = 0
                self.totals.append(0)
                # print("no btc pair:",i.currency, "%.8f"%float(i.available))
            # print(i.currency,t,"\n",self.totals,"\n")
        self.Total = sum(self.totals)
        print(self.User + "'s","Account Total:","%.8f"%self.Total,"BTC")
        return self.Total

    def check_market(self, product_pair):
        '''checks the market'''
        book = self.Client.get_product_order_book(product_pair)
        for k,v in book.items():
            if k == "bids":
                bid = float(v[0][0])
            if k == "asks":
                ask = float(v[0][0])
        return round((bid+ask)/2, 8)
        
    def make_trade(self, product_pair, side, size, price):
        for a in self.AvailableAccounts:
            # print(a)
            if a[0] in product_pair.split("-"):
                # print(a[0])
                for i in self.ProductMins:

                    if i[0] == product_pair:
                        # print(i[0])
                        if float(i[1]) <= size <= float(a[1]):
                            # print(i[1],a[1])
                            print("Sending " + side + " Trade On", product_pair + " @ " + "%.8f"%price + " with " + str(size), product_pair.split("-",0))
                            self.trade = self.Client.place_order(
                                product_id= product_pair,
                                side= side, 
                                order_type= 'limit',
                                price= price , 
                                size= size)
                            print("\nTrade Request Sent!")
                            for k,v in self.trade.items():
                                print(k,"=\t",v)
                            self.lastTrade = True
                        else:
                            pass
                    else:
                        pass
            else:
                pass

    def percent(self, cp, sp):
        if cp > sp:
            increase = cp - sp
            percent = (increase / sp) * 100
            x = [percent, "increase"]
        elif cp < sp:
            decrease = sp - cp
            percent = (decrease / sp) * 100
            x = [percent, "decrease"]
        else:
            x = [0,'null']
        return x

    def grabAccounts(self, product_pair: str):
        b,q = product_pair.split("-")
        for i in self.Accounts:
            if i.currency == b:
                base = i
            if i.currency == q:
                quote = i
        return [base,quote]
                        
    def auto_trade(self, product_pair:str, minutes:float, buy_limit:float, sell_limit:float, size:float, maxTrades:int = 4):
        '''auto_trade() Trades Automaticly based on provided inputs
                    product_pair  :   str   =  "BTC-USD", "ETH-BTC"
                         minutes  :  float  =  60*5 - 5 Hours
                       buy_limit  :  float  =  1.5 % decrease in price
                      sell_limit  :  float  =  1.5 % increase in price
                            size  :  float  =  0.0001 - size in (base currency) you want to use for each trade
                       maxTrades  :   int   =  Max Trades Made Per Side 
                            (maxTrades defaults to 4 if not otherwise specified)'''
        print(f'Start Time = {datetime.utcnow()}')
        sp = self.check_market(product_pair)
        stime = round(time.time())
        etime = stime + minutes * 60

        # last of things start empty
        trades = 0
        last_percent = 0
        last_difference = 'null'

        # Start of auto_trade loop
        while etime - round(time.time()) >= 0:
            cp = self.check_market(product_pair)
            change = self.percent(cp, sp)

            # if percent and difference are not default
            if change[0] > 0.01 and change[1] != "null":
                per = round(change[0],4)
                dif = change[1]

                # Debug
                # print(f'\n{cp:.8f}, {sp:.8f}')
                # print(f'{per:.8f}, {dif =}')
                # print(f'{change =}')

                # if percent is even high enough to care
                if per > 0.50:

                    # if per is not the same as the last time we checked
                    if round(per,4) >= last_percent:
                        print(f'\nStart Price {sp:.8f}.\nCurrent Price {cp:.8f}.\nChange {per:.4f}%.')
                        last_percent = per
                    print(f"\nwe have {dif}d {per}%")
                    base, quote = self.grabAccounts(product_pair)
                    for i in self.ProductMins:
                        if i[0] == product_pair:
                            minTradeSize = float(i[1])
                            fee = cp*.005
                            sellMIN = minTradeSize*size
                            buyMIN = ((minTradeSize*cp)+fee)
                        else:
                            minTradeSize = None

                    # INCREASED - Sell Checks
                    if dif == 'increase':
                        side = "sell"
                        last_difference = dif
                        if per >= sell_limit and trades <= maxTrades and float(base.available) >= sellMIN:
                            trades += 1
                            self.make_trade(product_pair,side,size,cp)
                            if self.lastTrade:
                                sp = self.check_market(product_pair)
                                self.lastTrade = False
                    
                    # DECREASED - Buy Checks
                    if dif == 'decrease':
                        side = "buy"   
                        last_difference = dif
                        if per >= buy_limit and trades <= maxTrades and float(quote.available) >= buyMIN:
                            trades += 1
                            self.make_trade(product_pair,side,size,cp)
                            if self.lastTrade:
                                sp = self.check_market(product_pair)
                                self.lastTrade = False

                    # TRADE SECURITY - Max Trades Check - Trade Sides
                    if trades >= maxTrades:
                        print("maxTrades Reached!")
                        trades = 9999
                        if last_difference != dif:
                            trades = 0
                    # Debug
                    #print(f'{last_difference = }, {dif = }')
            else:   
                # Debug    
                #print(f'Same Price {cp:.8f}')
                time.sleep(3)
            time.sleep(1)
        else: 
            # once the loop finishes
            print("Finished")

    def quick_fib_trade():
        pass

    def trade_total(self):
        pass