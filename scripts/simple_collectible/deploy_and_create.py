from scripts.utils import get_account, OPENSEA_URL
from brownie import config, network, SimpleCollectable


sample_token_uri = (
    "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
)


def deploy_and_create():
    account = get_account()
    simple_collectable = SimpleCollectable.deploy({"from": account})
    tx = simple_collectable.createCollectable(
        sample_token_uri,
        {"from": account},
    )
    tx.wait(1)
    print(
        f"You have deployed your nft to {OPENSEA_URL.format(simple_collectable.address, simple_collectable.tokenCounter() - 1)}"
    )
    return simple_collectable


def main():
    deploy_and_create()
