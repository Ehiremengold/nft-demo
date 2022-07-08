from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from scripts.utils import get_account, local_dev_env, get_contract

from brownie import network, exceptions
import pytest


def test_can_create_advanced_collectible():
    if network.show_active() not in local_dev_env:
        pytest.skip("Only for local testing")
    advanced_collectible, creating_tx = deploy_and_create()
    requestId = creating_tx.events["requestCollectible"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, advanced_collectible.address, {"from": get_account()}
    )

    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3
