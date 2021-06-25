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