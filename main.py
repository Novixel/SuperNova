# import envVars.env 
# we import this to set enviroment variables (provides for easy switching of portfolios)

# ### Debug #########
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
    man = Manager(con) # Manage Users Coinbase Portfolio
    # Return The Connected Manager
    return man

if __name__ == "__main__":
    # Create The Manager
    x = main()

    # Set Product For Trade!
    PRODUCT_ID = "BTC-USDC"

    # Grab The Accounts We Are Gonna Use!
    base, quote, pairs,  = x.check_Pair(PRODUCT_ID)
                    

    # print(x.NONPairs)
    # print(x.BTCPairs)

    # for i in range(len(x.Accounts)):
    #    print(i, x.Accounts[i].currency)

    # for i in range(len(x.Products)):
    #    print(i, x.Products[i].id)