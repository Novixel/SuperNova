from data.items import AccountItem , ProductItem
import time
from datetime import datetime

class Manager():
    '''We Call The Shots Around Here!
    
    Provide Me With An Authenticated User!
    
    '''
    Accounts : list = []
    Products : list = []
    BTCPairs : list = []
    NONPairs : list = []

    Available : list = []

    def __init__(self, connect):
        '''Connection Object, opt: True  = auto getTotals'''
        self.Connection = connect
        self.User = self.Connection.name
        self.Client = self.Connection.client()
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

    def check_Pair(self, product_id):
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
                    base = i
                if i.currency == q:
                    quote = i
            print("\tAvailable For Trade!")
            print("\t%.8f"%base.available, base.currency)
            print("\t%.8f"%quote.available, quote.currency)
            print(base.currency,"/",quote.currency,"pair : BTC | NON\n\t        ",BTCPair,"|",NONPair)

        return base , quote , [BTCPair, NONPair]


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