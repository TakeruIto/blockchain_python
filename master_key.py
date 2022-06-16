import os
import binascii
import ecdsa
import hmac
import hashlib

from rsa import PublicKey

seed = os.urandom(32)
root_key = b"Bitcoin seed"

def hmac_sha512(data, keymessage):
    hash = hmac.new(data, keymessage, hashlib.sha512).digest()
    return hash

def create_pubkey(private_key):
    publickey = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1).verifying_key.to_string()
    return publickey

master = hmac_sha512(seed, root_key)
master_secretkey = master[:32]
master_chaincode = master[32:]
master_publickey = create_pubkey(master_secretkey)

master_publickey_integer = int.from_bytes(master_publickey[32:], byteorder="big")

if master_publickey_integer%2==0:
    master_publickey_x = b"\x02" + master_publickey[:32]
else:
    master_publickey_x = b"\x03" + master_publickey[:32]

print("master private key")
print(binascii.hexlify(master_secretkey))
print("\n")
print("master chain code")
print(binascii.hexlify(master_chaincode))
print("\n")
print("master public key")
print(binascii.hexlify(master_publickey_x))

# -------------------------------

index = 0
index_bytes = index.to_bytes(8, "big")
data = master_publickey_x + index_bytes
result_hmac512 = hmac_sha512(data, master_chaincode)

sum_integer = int.from_bytes(master_secretkey, "big") + int.from_bytes(result_hmac512[:32], "big")

p = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1
child_secretkey = (sum_integer % p).to_bytes(32, "big")
print("\n")
print("child private key")
print(binascii.hexlify(child_secretkey))
