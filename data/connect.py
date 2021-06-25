# Connect To An Authenticated Coinbase Pro Portfolio API
import cbpro
from dataclasses import dataclass, field

@dataclass(frozen=True, order=True)
class Connect:
    '''Class for Connecting to Coinbase Pro'''
    name: str = field(default="Default")
    api: list[str,str,str] = field(default_factory=list, compare=False, repr=False )
    def client(self) -> cbpro.AuthenticatedClient:
        '''This client provides all the functions to talk with coinbase'''
        print("Initalizing",self.name)
        return cbpro.AuthenticatedClient(self.api[0],self.api[1],self.api[2])