from time import sleep
import envVars.env 
# we import this to set enviroment variables

from data.connect import Connect
from data.manager import Manager
from data.user import User
from datetime import datetime

def man():
    '''User() + Connect(User.name, User.api) = Authenticated_Client -> returns Manager(Authenticated_Client)'''
    user = User() # Collect User Data From Enviroment
    con = Connect(user.name, user.api ) # Connect User To Coinbase API
    # Return The Connected Manager
    return Manager(con)

def autoTrade(manager:Manager):
    product_id:str = "BTC-USDC"
    minSell:int = 2
    maxSell:int = 10
    minBuy:int = 2
    maxBuy:int = 10
    Max_Loops:int = 60*12
    trades = manager.Auto_Trader(product_id,minSell,maxSell,minBuy,maxBuy,Max_Loops)
    for i in trades:
        print(i)
    return trades

def main():
    x = man()
    start = True
    trades = None
    while start:
        getTime = datetime.utcnow()
        disTime = getTime.strftime("%c")
        if getTime.minute % 5 == 0:
            print("Bot Starting :",disTime)
            trades = autoTrade(x)
            start = True if input("Start Again?\ny/n: ") in ["yes","y","ye","yup",] else start = False
    else:
        getTime = datetime.utcnow()
        disTime = getTime.strftime("%c")
        with open((disTime + "trades.txt"),"w") as a:
            a.write(trades)
        print('saved to file',disTime)
        
if __name__ == "__main__":
    main()



    