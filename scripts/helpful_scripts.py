from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

LOCAL_FORKED_ENVIORMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_DEPLOYMENT_ENVIORNMENTS = ["development", "ganache-local"]

DECIMALS = 8
STARTING_PRICE = 200_000_000_000


def get_account(index=0):
    if (
        network.show_active() in LOCAL_DEPLOYMENT_ENVIORNMENTS
        or network.show_active() in LOCAL_FORKED_ENVIORMENTS
    ):
        return accounts[index]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is '{network.show_active()}'.")
    print("Deploying Mocks ...")
    if len(MockV3Aggregator) <= 0:  # If there are none deployed yet.
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print("Mocks deployed!")
