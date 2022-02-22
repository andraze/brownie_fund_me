from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    LOCAL_DEPLOYMENT_ENVIORNMENTS,
    deploy_mocks,
    get_account,
)
from web3 import Web3


def deploy_fund_me(index=0):
    account = get_account(index)
    # Pass the feed address to our FundMe contract
    # If we are on a persistent network like rinkeby, use the associated address,
    # otherwise, deploy mocks.
    print(f"Current network = {network.show_active()}")
    if network.show_active() not in LOCAL_DEPLOYMENT_ENVIORNMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
