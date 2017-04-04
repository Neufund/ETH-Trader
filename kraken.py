from decimal import Decimal

import requests

PAIR = "XETHZEUR"


def fetch_bids():
    orders = requests.get("https://api.kraken.com/0/public/Depth", params={"pair": PAIR})
    data = orders.json()
    return data["result"][PAIR]["bids"]


def get_price(bids, amount):
    price = 0
    for bid_price, bid_size, _ in bids:
        bid_price = Decimal(bid_price)
        bid_size = Decimal(bid_size)
        buys = min(amount, bid_size)
        pays = buys * bid_price
        price += pays
        amount -= buys
    assert amount == 0
    return price
