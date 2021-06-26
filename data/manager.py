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
    ATH = 64899.00
    
    # Lists
    Accounts : list = []
    Products : list = []
    BTCPairs : list = []
    NONPairs : list = []

    # Active List
    Available : list = []

    # Trade Variables
    last_trade_id : str = 'trade_id'
    last_trade_price : float = 0
    last_trade_side : BUY or SELL
    last_trade_size : float = 0

    def __init__(self, connect):
        '''Connection Object, opt: True  = auto getTotals'''
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

    def Trade(self, product_id, side, price, size):
        '''Send Limit Trade Request'''
        # Place The Trade
        trade = self.Client.place_limit_order(product_id, side, price, size)
        # Set Recent Trade Variables
        self.last_trade_id = str(trade["id"])
        self.last_trade_side = str(trade["side"])
        self.last_trade_price = float(trade["price"])
        self.last_trade_size = float(trade["size"])
        return trade

    def Quick_Trade(self, product_id:str, side, size):
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

    def Safe_Trade(self, product_id, side, price, size):
        # Check The Order
        if self.last_trade_id != 'trade_id':
            last_order = self.Client.get_order(self.last_trade_id)
        # and Status
        if last_order['status'] == 'open':
            print("last order is open!")
            return last_order
        elif last_order['status'] == 'done':
            print("last order is done")
        else:
            trade = self.Trade(product_id,side,price,size)
            # Grab That Trade From The Order Book
            return self.Client.get_order(trade["id"])

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


    def make_trade(self, product_pair, side, size, price):
        print("Sending " + side + " Trade On", product_pair + " @ " + "%.8f"%price + " with " + str(size), product_pair.split("-",0))
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