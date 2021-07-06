

from time import localtime
from data.items import AccountItem, ProductItem
from dataclasses import asdict
import envVars.tenv 

from data.connect import Connect
from data.manager import Manager
from data.user import User
from datetime import datetime

def CheckTrade(man:Manager,Base:AccountItem,Quote:AccountItem,Product:ProductItem):
    '''For the razz pi to use'''
    Debug = True
    if Base.available > Product.base_min_size or Debug == True:
        ticker = man.Client.get_product_ticker(Product.id)
        dayTick = man.Client.get_product_24hr_stats(Product.id)
        high = float(dayTick['high'])
        low = float(dayTick['low'])
        current = float(ticker['price'])
        topBase = (current + high) / 2
        botBase = (current + low) / 2
        hchange = (high - current)/high * 100
        lchange = (current - low)/low * 100
        if Debug:
            print("\tTicker:\n",ticker)
            print("\t24HourStats:\n",dayTick)
            print(f'''\t\tStats:
                {high = }
             {topBase = }
               change = {hchange:.2f}%
             {current = }
               change = {lchange:.2f}%
             {botBase = }
                 {low = }
                ''')

    else:
        print('Please Add More Funds To Your Account In Order To Start Trading!')
        exit()

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
    base, quote, product = man.check_Pair(product_id)
    return base,quote,product,man

if __name__ == "__main__":
    Base , Quote, Product, Man, = main()
    CheckTrade(Man,Base,Quote,Product)
    

