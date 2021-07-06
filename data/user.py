import os 

class User:
    def __init__(self):
        # Set This On Your Machine
        a = os.environ["API_KEY"]
        b = os.environ["API_SECRET"]
        c = os.environ["API_PASS"]
        d = os.environ["USER"]
        self.api = [a,b,c]
        self.name = d

    def SaveUser(self):
        username = self.name
        password = input('set a secure password') or None
        if password is not None:
            with open((username+".usr"),"w") as user:
                user.writelines([username+"\n",password])