#!/usr/bin/env python3

# Init SuperNova Package
import supernova as nov 
from types import SimpleNamespace

# Constants 
name = "Novixel"

# Start the app
user = nov.Client(name)
user.Connect()

currencys = user.client.get_currencies()

print(curs)
