from cbpro.authenticated_client import AuthenticatedClient
from data.items import AccountItem , ProductItem
import time
from datetime import datetime

class Manager():
    '''We Call The Shots Around Here!
    
    Provide Me With An Authenticated User!
    
    '''
    # Constants
    BUY = 'buy'
    SELL = 'sell'
    
    # Lists
    Accounts : list = []
    Products : list = []
    BTCPairs : list = []
    NONPairs : list = []

    # Active List
    Available : list = []

    # Trade Variables
    last_trade_id : str
    last_trade_price : float = 0
    last_trade_side : BUY or SELL
    last_trade_size : float = 0
    last_filled : dict

    def __init__(self, connect):
        '''Connection Object'''
        self.Connection = connect
        self.User = self.Connection.name
        self.Client : AuthenticatedClient = self.Connection.client()
        self.__getAccounts()
        self.__getProducts()
        self.__getTradable()
    
    def __getAccounts(self):
        Acc = self.Client.get_accounts()
        self.Accounts = []
        for a in Acc:
            self.Accounts.append(AccountItem(a))

    def __getProducts(self):
        pros = self.Client.get_products()
        self.Products = []
        for a in pros:
            self.Products.append(ProductItem(a))

    def __getTradable(self):
        for i in range(len(self.Accounts)):
            if self.Accounts[i].available > 0:
                self.Available.append(self.Accounts[i])
        for i in range(len(self.Products)):
            if "BTC" in self.Products[i].id.split("-"):
                self.BTCPairs.append(self.Products[i])
            elif "BTC" not in self.Products[i].id.split("-"):
                self.NONPairs.append(self.Products[i])
            else:
                print("Tradable product error :",self.Products[i])
                raise ValueError

    def ShowAccounts(self):
        '''Show All Accounts!'''
        for i in range(len(self.Accounts)):
           print(i, self.Accounts[i].currency)

    def ShowProducts(self):
        '''Show All Products!'''
        for i in range(len(self.Products)):
           print(i, self.Products[i].id)
    
    def ShowBTCPairs(self):
        '''Show Sorted BTC Product Pairs!'''
        for i in range(len(self.BTCPairs)):
           print(i, self.BTCPairs[i].id)

    def ShowNONPairs(self):
        '''Show Sorted NON BTC Product Pairs!'''
        for i in range(len(self.NONPairs)):
           print(i, self.NONPairs[i].id)

    def ShowAvailable(self):
        '''Show All Available Products!'''
        for i in range(len(self.Available)):
           print(i,"%.8f"%self.Available[i].available, self.Available[i].currency)

    def UpdateAccount(self,a:AccountItem):
        new = self.Client.get_account(a.id)
        a.update(new)

    def getBidAsk(self, product_id):
        book = self.Client.get_product_order_book(product_id)
        for k,v in book.items():
            if k == "bids":
                bid = float(v[0][0])
            if k == "asks":
                ask = float(v[0][0])
        return bid, ask

    def Spec_Trader(self, product_id:str, Hours:float, buy_limit:float, sell_limit:float, size:float, maxTrades:int = 4):
        '''Checks Market Every 5 Min On The Min!'''
        base, quote, product = self.check_Pair(product_id)
        Total_Loops = 0
        stime = round(time.time())
        etime = stime + Hours * 60
        Trades = []
        curTrades = 0
        tick = self.Client.get_product_ticker(product_id)
        Start_Price = float(tick['price'])
        while etime - round(time.time()) >= 0:
            # Benchtime and Local Time
            starttime = time.perf_counter()
            print("\nStarted:",datetime.utcnow().strftime("%c"),"\n")

            # Gather Market Info
            bid, ask = self.getBidAsk(product_id)
            current_price = (bid+ask)/2

            # Gather Last Filled Trade Info
            last_filled = self.get_last_fill(product_id)
            last_price = float(last_filled['price'])
            last_side = last_filled['side']

            # Percent Change
            change = (current_price - Start_Price)/Start_Price * 100
            trade_change = (current_price - last_price)/last_price * 100

            # Available Funding Check : How Many Trades Can We Make!
            if base.available >= product.base_min_size:
                Total_Sells = (base.available  // product.base_min_size)
            else:
                Total_Sells = 0 

            if quote.available > product.base_min_size * current_price:
                Total_Buys = (quote.available // (product.base_min_size * current_price))
            else:
                Total_Buys = 0

            BuyTrade = {'message': 'default'}
            SellTrade = {'message': 'default'}

            # Send trade if we can
            if Total_Buys > 0 and change <= buy_limit and last_price > bid:
                BuyTrade = self.Trade(product_id,self.BUY,bid,(product.base_min_size*size))

            if Total_Sells > 0 and change >= sell_limit and last_price < ask:
                SellTrade = self.Trade(product_id,self.SELL,ask,(product.base_min_size*size))

            if 'message' not in SellTrade.keys():
                Trades.append({SellTrade['side'],SellTrade['size'],SellTrade['price']})
                curTrades += 1
                if maxTrades <= curTrades:
                    print("resetting Start Price")
                    Start_Price = current_price
                    curTrades = 0

            if 'message' not in BuyTrade.keys():
                Trades.append({BuyTrade['side'],BuyTrade['size'],BuyTrade['price']})
                curTrades += 1
                if maxTrades <= curTrades:
                    print("resetting Start Price")
                    Start_Price = current_price
                    curTrades = 0

            # Debug info
            print(f"{Total_Sells = }, {Total_Buys = }")
            print(f"        Last Trade Side     = {last_side}")
            print(f"        Last Trade Change   = {current_price - last_price:.8f}, {quote.currency}")
            print(f"        Last Trade Percent  = {trade_change:.2f}%\n")
            print(f" bid: {bid:.2f}, ask: {ask:.2f}, spread: {bid-ask:.2f}, current: {current_price}")
            print(f"        Amount Change  = {current_price - Start_Price:.2f} {quote.currency}")
            print(f"        Percent Change = {change:.2f}%\n")
            print(f"    Current Base  = {base.available:.8f} {base.currency}")
            print(f"    Current Quote = {quote.available:.2f} {quote.currency} ")
            print("Trades:",Trades)

            # Loop Counter & Account Updates
            Total_Loops += 1
            self.UpdateAccount(base)
            self.UpdateAccount(quote)
            # if datetime.utcnow().minute % 5 == 0:
            #     pass
            # benchtime & nap
            endtime = time.perf_counter()
            print(f"\nLoop completed in {endtime - starttime:.2f}s",)
            time.sleep((60 - (endtime - starttime)))
        else:
            # End Of While Loop! Retrun Our Profit To The Manager!
            print("Ended:",datetime.utcnow().strftime("%c"),"\n")
            return Trades

    def Auto_Trader(self,product_id, Max_Loops:int):
        '''Checks Market Every 5 Min On The Min!'''
        base, quote, product = self.check_Pair(product_id)
        Total_Loops = 0
        Trades = []
        tick = self.Client.get_product_ticker(product_id)
        Start_Price = float(tick['price'])
        while Total_Loops < Max_Loops:
            # Benchtime and Local Time
            starttime = time.perf_counter()
            print("\nStarted:",datetime.utcnow().strftime("%c"),"\n")

            # Gather Market Info
            bid, ask = self.getBidAsk(product_id)
            current_price = (bid+ask)/2

            # Gather Last Filled Trade Info
            last_filled = self.get_last_fill(product_id)
            last_price = float(last_filled['price'])
            last_side = last_filled['side']

            # Percent Change
            change = (current_price - Start_Price)/Start_Price * 100
            trade_change = (current_price - last_price)/last_price * 100

            # Available Funding Check : How Many Trades Can We Make!
            if base.available >= product.base_min_size:
                Total_Sells = (base.available  // product.base_min_size)
            else:
                Total_Sells = 0 

            if quote.available > product.base_min_size * current_price:
                Total_Buys = (quote.available // (product.base_min_size * current_price))
            else:
                Total_Buys = 0

            BuyTrade = {'message': 'default'}
            SellTrade = {'message': 'default'}

            # Send trade if we can
            if Total_Buys > 4 and change < -10.0:
                BuyTrade = self.Trade(product_id,self.BUY,bid,product.base_min_size*5)
            elif Total_Buys > 2 and change < -5.0:
                BuyTrade = self.Trade(product_id,self.BUY,bid,(product.base_min_size*3))
            elif Total_Buys > 1 and change < -2.0 and last_price > bid:
                BuyTrade = self.Trade(product_id,self.BUY,bid,(product.base_min_size*2))
            elif Total_Buys > 0 and change < -1.25 and last_price > bid:
                BuyTrade = self.Trade(product_id,self.BUY,bid,(product.base_min_size))

            if Total_Sells > 4 and change > 10.0:
                SellTrade = self.Trade(product_id,self.SELL,ask,product.base_min_size*5)
            elif Total_Sells > 2 and change > 5.0:
                SellTrade = self.Trade(product_id,self.SELL,ask,(product.base_min_size*3))
            elif Total_Sells > 1 and change > 2.5 and last_price < ask:
                SellTrade = self.Trade(product_id,self.SELL,ask,(product.base_min_size*2))
            elif Total_Sells > 0 and change > 2 and last_price < ask:
                SellTrade = self.Trade(product_id,self.SELL,ask,(product.base_min_size))

            if 'message' not in SellTrade.keys():
                Trades.append({SellTrade['side'],SellTrade['size'],SellTrade['price']})
                Start_Price = current_price

            if 'message' not in BuyTrade.keys():
                Trades.append({BuyTrade['side'],BuyTrade['size'],BuyTrade['price']})
                Start_Price = current_price

            # Debug info
            print(f"{Total_Sells = }, {Total_Buys = }")
            print(f"        Last Trade Side     = {last_side}")
            print(f"        Last Trade Change   = {current_price - last_price:.8f}, {quote.currency}")
            print(f"        Last Trade Percent  = {trade_change:.2f}%\n")
            print(f" bid: {bid:.2f}, ask: {ask:.2f}, spread: {bid-ask:.2f}, current: {current_price}")
            print(f"        Amount Change  = {current_price - Start_Price:.2f} {quote.currency}")
            print(f"        Percent Change = {change:.2f}%\n")
            print(f"    Current Base  = {base.available:.8f} {base.currency}")
            print(f"    Current Quote = {quote.available:.2f} {quote.currency} ")
            print("Trades:",Trades)

            # Loop Counter & Account Updates
            Total_Loops += 1
            self.UpdateAccount(base)
            self.UpdateAccount(quote)
            # if datetime.utcnow().minute % 5 == 0:
            #     pass
            # benchtime & nap
            endtime = time.perf_counter()
            print(f"\nLoop completed in {endtime - starttime:.2f}s",)
            time.sleep((60 - (endtime - starttime)))
        else:
            # End Of While Loop! Retrun Our Profit To The Manager!
            print("Ended:",datetime.utcnow().strftime("%c"),"\n")
            return Trades

    def Trade(self, product_id, side, price, size):
        '''Send Limit Trade Request'''
        # Place The Trade
        trade: dict = self.Client.place_limit_order(product_id, side, price, size)
        # Set Recent Trade Variables
        if 'message' in trade.keys():
            print(trade)
        else:
            self.last_trade_id = str(trade["id"])
            self.last_trade_side = str(trade["side"])
            self.last_trade_price = float(trade["price"])
            self.last_trade_size = float(trade["size"])
        return trade

    def Market_Trade(self, product_id, side, size):
        # Get Current Market Price
        price = float(self.Client.get_product_ticker(product_id)['price'])
        # Place The Trade
        if side == self.BUY:
            trade = self.Trade(product_id, self.BUY, price, size)
            order = self.Client.get_order(trade["id"])
            return order
        elif side == self.SELL:
            trade = self.Trade(product_id, self.SELL, price, size)
            order = self.Client.get_order(trade["id"])
            return order

    def get_last_fill(self, product_id):
        fills = self.Client.get_fills(product_id)
        for i in fills:
            self.last_filled = i
            break
        return self.last_filled

    def check_Pair(self, product_id):
        '''Check Product Pair Before You Trade! 
        -> BaseItem, QuoteItem, ProductItem'''
        for i in range(len(self.Products)):
           if product_id == self.Products[i].id:
               product : ProductItem = self.Products[i]

        if any(p.id == product_id for p in self.BTCPairs):
            BTCPair = True
        else:
            BTCPair = False

        if any(p.id == product_id for p in self.NONPairs):
            NONPair = True
        else:
            NONPair = False

        base = object
        quote = object
        
        if BTCPair or NONPair:
            b,q =  product_id.split("-")
            for i in self.Available:
                if i.currency == b:
                    base : AccountItem = i
                if i.currency == q:
                    quote : AccountItem = i
            print("\tAvailable For Trade!")
            print("\t%.8f"%base.available, base.currency)
            print("\t%.8f"%quote.available, quote.currency)
            print(base.currency,"/",quote.currency,"pair : BTC | NON\n\t        ",BTCPair,"|",NONPair)
            print("Minumum Trade Size:",product.base_min_size,base.currency)
        else:
            raise ValueError("Product Error!",product_id + " is not a valid product!")

        return base, quote, product

    def getBalance(self, base:AccountItem, quote:AccountItem, product_id:str):
        '''Get balances for product'''
        base_bal, quote_bal = base.available, quote.available
        price = self.Client.get_product_ticker(product_id)
        start_bal = base_bal + (quote_bal / float(price["price"]))
        print("(BASE)  Total Balance:",start_bal, base.currency)
        print("(QUOTE) Total Balance:",start_bal * float(price["price"]), quote.currency)
        return base_bal, quote_bal , start_bal

    def fake_trade(self, product_pair, side, size, price):
        print("Sending " + side + " Trade On", product_pair + " @ " + "%.8f"%price + " with " + str(size), product_pair.split("-",0))
        return side, size, price
        # self.trade = self.Client.place_order(
        #     product_id= product_pair,
        #     side= side, 
        #     order_type= 'limit',
        #     price= price , 
        #     size= size
        #     )
        # print("\nTrade Request Sent!")
        # for k,v in self.trade.items():
        #     print(k,"=\t",v)