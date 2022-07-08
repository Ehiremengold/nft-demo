from scripts.simple_collectible.deploy_and_create import deploy_and_create
from scripts.utils import get_account, local_dev_env

# from scripts.deploy_and_create import SimpleCollectable
from brownie import network, exceptions
import pytest


def test_can_create_simple_collectible():
    if network.show_active() not in local_dev_env:
        pytest.skip("only for local testing")
    simple_collectible = deploy_and_create()
    assert simple_collectible.ownerOf(0) == get_account()
