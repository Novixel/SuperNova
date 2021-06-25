# Coinbase Pro Account Manager
# Codename: Algorand
# Author: Tristan "Novixel"
# v0.10
# main.py

import envVars.env 
# we import this to set enviroment variables (provides for easy switching of portfolios)
from data.connect import Connect
from data.manager import Manager
from data.user import User

def main():
    '''User() + Connect(User.name, User.api) = Authenticated_Client -> returns Manager(Authenticated_Client)'''
    user = User()
    con = Connect(user.name, user.api )
    man = Manager(con, True)
    # Lets get Our Manager To Do Somthing!
    return man

if __name__ == "__main__":
    # constants for automation
    pair = 'ALGO-BTC'
    size = 2
    minutes = 15
    buy_limit = 1.6
    sell_limit = 1.6

    # establish user account
    x = main()

    startTotal = x.Total
    # base, quote = x.grabAccounts(pair)

    # print(base.currency)
    # print(quote.currency)

    # auto trade timings
    x.auto_trade(pair, minutes, buy_limit, sell_limit, size , maxTrades=5)

    endTotal = x.getTotal()

    finalProfit = endTotal - startTotal

    print(f'{startTotal:.8f} - {endTotal:.8f} = {finalProfit:.8f}')
    print("Total Profit %.8f"%finalProfit)
    # check the market for fun
    # p = x.check_market(pair)

    # test for manual trade
        #x.make_trade(pair,'buy', size, p)
        #x.make_trade(pair,'sell', size, p)