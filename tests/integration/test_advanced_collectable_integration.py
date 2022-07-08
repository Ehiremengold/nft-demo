from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from scripts.utils import get_account, local_dev_env, get_contract
import time
from brownie import network, exceptions
import pytest


def test_can_create_advanced_collectible_integration():
    if network.show_active() in local_dev_env:
        pytest.skip("Only for integration testing")
    advanced_collectible, creating_tx = deploy_and_create()
    time.sleep(200)
    assert advanced_collectible.tokenCounter() == 1