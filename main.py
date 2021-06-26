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


def main():
    '''User() + Connect(User.name, User.api) = Authenticated_Client -> returns Manager(Authenticated_Client)'''
    user = User() # Collect User Data From Enviroment
    con = Connect(user.name, user.api ) # Connect User To Coinbase API
    # Return The Connected Manager
    return Manager(con)

def fills(x:Manager,base:AccountItem, quote:AccountItem, product:ProductItem):
    fills = x.Client.get_fills(product.id)
    for i in fills:
        last_filled = i
        break
    print(last_filled["price"])


if __name__ == "__main__":
    # Call The Manager To Work
    x = main()

    # Set Product For Trade
    PRODUCT_ID = "BTC-USDC"

    # Grab The Accounts From Our Product Pair
    base, quote, product  = x.check_Pair(PRODUCT_ID)

    # Get Mininum Trade Size
    BASEMIN = product.base_min_size
    QUOTEMIN = product.min_market_funds

    # Make Test Trade
    for i in range(3):
        trade_order = x.Attempt_Trade(product_id=PRODUCT_ID, side=x.SELL, price=x.ATH ,size=BASEMIN)
        print(trade_order)
    # We Can Grab Balances Seperatly If We Need to Do Other Math
    # base_bal, quote_bal , start_bal = x.getBalance(base, quote, PRODUCT_ID)



    