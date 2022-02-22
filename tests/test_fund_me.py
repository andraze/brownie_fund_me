from scripts.helpful_scripts import LOCAL_DEPLOYMENT_ENVIORNMENTS, get_account
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    ## Prepare
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()
    ## Execute 1
    transaction_fund = fund_me.fund({"from": account, "value": entrance_fee})
    transaction_fund.wait(1)
    ## Assert 1
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    ## Execute 2
    transaction_withdraw = fund_me.withdraw({"from": account})
    transaction_withdraw.wait(1)
    ## Assert 2
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner():
    if network.show_active() not in LOCAL_DEPLOYMENT_ENVIORNMENTS:
        pytest.skip("Only for local testing!")
    bad_actor = accounts.add()
    fund_me = deploy_fund_me()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
