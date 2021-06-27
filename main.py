# import envVars.env 
# we import this to set enviroment variables (provides for easy switching of portfolios)

# ### Debug #########
from data.items import AccountItem, ProductItem
from dataclasses import asdict
import envVars.tenv #
#####################

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

def main():
    # import cProfile
    # import pstats

    # with cProfile.Profile() as pr:
    #     man()
    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()

    x = man()
    # Set Product For Trade
    PRODUCT_ID = "BTC-USDC"
    MAX_LOOPS = 60*8

    # Grab The Accounts From Our Product Pair
    # base, quote, product  = x.check_Pair(PRODUCT_ID)

    # Testing Auto Trade
    profit, trades = x.Auto_Trader(PRODUCT_ID,MAX_LOOPS)

    for i in trades:
        print(i)

if __name__ == "__main__":
    main()



    