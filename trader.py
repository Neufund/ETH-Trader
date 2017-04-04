import json
import logging
import os
import signal
from pprint import pprint

from web3 import HTTPProvider, Web3

from kraken import fetch_bids, get_price

ETH_EUR_TRADER_ARTIFACTS_PATH = "Contracts/build/contracts/EthEurTrader.json"
EURO_TOKENS_FOR_EURO = 100


def init_web3():
    web3 = Web3(HTTPProvider(endpoint_uri=os.environ["ENDPOINT_URI"]))
    pk_manager = Web3.PrivateKeySigningManager(web3._requestManager)
    private_key = bytes.fromhex(os.environ["PRIVATE_KEY"])
    pk_manager.register_private_key(private_key)
    address = list(pk_manager.keys)[0]
    web3.setManager(pk_manager)
    web3.eth.defaultAccount = address
    return web3


web3 = init_web3()


def create_contract_from_truffle_artifacts(path):
    with open(path) as contract:
        kyc_spec_json = json.load(contract)
    abi = kyc_spec_json["abi"]
    address = kyc_spec_json["networks"][str(web3.version.network)]["address"]
    return web3.eth.contract(abi, address)


def on_eth_received(event):
    eth_amount = Web3.fromWei(event["args"]["amount"], "ether")
    client_address = event["args"]["client"]
    logging.info("Received {} ether from {}".format(eth_amount, client_address))
    logging.info("Fetching bids...")
    bids = fetch_bids()
    logging.info(
        "Bids fetched. Overall bid cap is: {} ETH".format(sum(float(size) for _, size, _ in bids)))
    eur_amount = get_price(bids, eth_amount)
    logging.info("Would sell {} ETH for {} EUR. Price: {}".format(eth_amount, eur_amount,
                                                                  eur_amount / eth_amount))
    # TODO Do actual trading
    eur_tokens = int(eur_amount * EURO_TOKENS_FOR_EURO)
    logging.info("Transfer {} EUR Tokens...".format(eur_tokens))
    tx = traderContract.transact().traded(client_address, eur_tokens)
    logging.info("Submitted transaction: {}".format(tx))


traderContract = create_contract_from_truffle_artifacts(ETH_EUR_TRADER_ARTIFACTS_PATH)

traderEventFilter = traderContract.on("EthReceived")


def start_watching():
    traderEventFilter.watch(on_eth_received)


def stop_watching(*_):
    print("Stop watching")
    traderEventFilter.stop_watching()


# On exit unregister filters
signal.signal(signal.SIGINT, stop_watching)
