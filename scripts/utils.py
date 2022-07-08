from threading import local

from web3 import Web3
from brownie import accounts, network, config, VRFCoordinatorMock, LinkToken, Contract

forked_dev_env = ["mainnet-fork"]

local_dev_env = ["development", "mainnet-fork", "ganache", "hardhat"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
BREED_MAPPING = {0:"PUG", 1:"SHIBA_INU", 2:"ST_BERNARD"}

def get_breed(breed_number):
    return BREED_MAPPING[breed_number]
    
def get_account(id=None, index=None):
    if id:
        return accounts.load(id)
    if index:
        return accounts[index]
    if network.show_active() in local_dev_env:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


contracts_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def deploy_mocks():
    account = get_account()
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})


def get_contract(contract_name):

    contract_type = contracts_to_mock[contract_name]

    if network.show_active() in local_dev_env:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]

        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(1, "ether")
):
    # amount = 0.1 Link
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    # account is equal to passsed account
    # in the function if its given else use get_account()
    # option A of interacting/transfering token to a contract
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    # or
    # option B of interacting/transfering token to a contract
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    # tx.wait(1)
    print("Contract funded with Link")
    return tx
