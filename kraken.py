from decimal import Decimal

import requests

PAIR = "XETHZEUR"


class TradeAmountTooHigh(OverflowError):
    pass


def fetch_bids():
    orders = requests.get("https://api.kraken.com/0/public/Depth", params={"pair": PAIR})
    data = orders.json()
    return data["result"][PAIR]["bids"]


def get_price(bids, amount):
    price = 0
    order_book_volume = sum(float(size) for _, size, _ in bids)
    if amount > order_book_volume:
        raise TradeAmountTooHigh(
            "Can't trade {} ETH for EUR. The amount is higher than the order book volume {}".format(
                amount, order_book_volume))
    for bid_price, bid_size, _ in bids:
        bid_price = Decimal(bid_price)
        bid_size = Decimal(bid_size)
        buys = min(amount, bid_size)
        pays = buys * bid_price
        price += pays
        amount -= buys
    return price
