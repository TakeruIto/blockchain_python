import json
import requests

address = "1EURH7eJgZmBH571vVhjTXBkgLTjGVEu5M"  # "3FkenCiXpSLqD8L79inRNXUgjRoH9sjXa"ではエラー発生

res = requests.get("https://blockchain.info/unspent?active=" + address)
utxo_list = json.loads(res.text)["unspent_outputs"]

print("Found " + str(len(utxo_list)) + " UTXOs")
for utxo in utxo_list:
    print(utxo["tx_hash"] + ":" + str(utxo["value"]) + " satoshis")