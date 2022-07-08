from brownie import AdvancedCollectible
from scripts.utils import fund_with_link, get_account
from web3 import Web3


def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible, amount=Web3.toWei(0.1, "ether"))
    creating_tx = advanced_collectible.createCollectable({"from": account})
    creating_tx.wait(1)
    print("New Collectible created...")
    return creating_tx
