import unittest
from decimal import Decimal
from unittest.mock import patch

from kraken import TradeAmountTooHigh, fetch_bids, get_price
from trader import on_eth_received

EVENT = {'address': '0xfeb1d5b757a40ad0f1fc71c1306ace85a890f4df',
         'args': {'amount': 1000000000000000000,
                  'client': '0x00817ee9d9c257560d682a42e01e6cfbe4bef37c'},
         'blockHash': '0xcc387389c93259df2a8f6c7eda47920e2237f46173d592eba48f7e9cb247e534',
         'blockNumber': 664321,
         'event': 'EthReceived',
         'logIndex': 0,
         'transactionHash': '0x204fd54ff6474bac0287d3f5d9110e0a9df725cb07159ef0d00c9a1bcd92c779',
         'transactionIndex': 0}
_ = None
BIDS = [
    [42, 1, _],
    [41, 2, _],
    [40, 2, _],
]


class EthTraderTest(unittest.TestCase):
    def test_fetch_bids(self):
        bids = fetch_bids()
        self.assertNotIn("result", bids)
        self.assertTrue(isinstance(bids, list))
        self.assertEqual(len(bids[0]), 3)

    def test_get_price(self):
        _ = None
        self.assertEqual(get_price(BIDS, 1), 42)
        self.assertEqual(get_price(BIDS, 2), 83)
        self.assertEqual(get_price(BIDS, 3), 124)
        self.assertEqual(get_price(BIDS, 5), 204)
        with self.assertRaises(TradeAmountTooHigh):
            get_price(BIDS, 6)

    @patch('trader.fetch_bids')
    @patch('trader.send_eur_tokens')
    def test_on_eth_received(self, send_tokens_mock, fetch_bids_mock):
        fetch_bids_mock.return_value = BIDS
        on_eth_received(EVENT)
        send_tokens_mock.assert_called_with("0x00817ee9d9c257560d682a42e01e6cfbe4bef37c",
                                            Decimal('42'))
