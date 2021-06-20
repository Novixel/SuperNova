import cbpro
class Client():
    Name = None
    def __init__(self, name):
        self.Name = name
    
    def Connect(self):
        self.client = cbpro.PublicClient()
        self.time = self.client.get_time()
        return