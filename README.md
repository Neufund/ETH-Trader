# Eth Trader

Eth trader watches the EthEurTrader smart contract 
for incoming transfers and trades Ether for Euro using Kraken API

It then notifies the contract and issues Euro tokens

## Cloning
This repo has submodules, so use `--recursive` while clonning

## Configuration
* `ENDPOINT_URI` - uri of the ETH node. Should support filters. (Not infura) 
* `PRIVATE_KEY` - private key of ETH Trader

## Runing
* Set config variables in config.env
* ```docker-compose up```

## Tests
* `pip install -r requirements.txt`
* set env config variables
* `py.test`
