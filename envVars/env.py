# Set Your Private API Keys Here
import os
os.environ["API_KEY"] = input('enter api key') or "Coinbase Pro Api Key"
os.environ["API_SECRET"] = input('enter api b64secret') or "Coinbase Pro Api b64Secret"
os.environ["API_PASS"] = input('enter api passphrase') or "Coinbase Pro Api Passphrase"
os.environ["USER"] = input('enter your username') or "Enter a Username"