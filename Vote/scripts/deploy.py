from brownie import Coin, accounts

def main():
    c = Coin.deploy({"from": accounts[0]})
