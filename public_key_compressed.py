import os 
import ecdsa
import binascii
private_key = os.urandom(32)
public_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1).verifying_key.to_string()

public_key_y = int.from_bytes(public_key[32:], "big")

if public_key_y%2==0:
    public_key_compressed = b"\x02" + public_key[:32]
else:
    public_key_compressed = b"\x03" + public_key[:32]

print(binascii.hexlify(public_key))
print(binascii.hexlify(public_key_compressed))