import logging
import signal

from trader import on_eth_received, start_watching

logging.basicConfig(level=logging.INFO)
start_watching()
signal.pause()
