import os 
import ecdsa
import binascii
private_key = os.urandom(32)
public_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1).verifying_key.to_string()

print(binascii.hexlify(private_key))
print(binascii.hexlify(public_key))