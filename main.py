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
    # Lets get Our Manager To Do Somthing!
    return man

if __name__ == "__main__":
    x = main()

    product_id = "BTC-USDC"

    if any(p.id == product_id for p in x.BTCPairs):
        print("BTCPair: True")
        BTCPair = True
    else:
        print("BTCPair: False")
        BTCPair = False

    if any(p.id == product_id for p in x.NONPairs):
        print("NONPair: True")
        NONPair = True
    else:
        print("NONPair: False")
        NONPair = False

    if BTCPair or NONPair:
        for i in x.Available:
            for k, v in asdict(i).items():
                print(k , v )

    # print(x.NONPairs)
    # print(x.BTCPairs)

    # for i in range(len(x.Accounts)):
    #    print(i, x.Accounts[i].currency)

    # for i in range(len(x.Products)):
    #    print(i, x.Products[i].id)