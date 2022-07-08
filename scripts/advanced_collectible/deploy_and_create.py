from brownie import config, network, AdvancedCollectible
from scripts.utils import (
    fund_with_link,
    get_account,
    get_contract,
    fund_with_link,
    local_dev_env,
)


def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    fund_with_link(advanced_collectible.address)
    creating_tx = advanced_collectible.createCollectable({"from": account})
    print("New Token Created...")
    return advanced_collectible, creating_tx


def main():
    deploy_and_create()
