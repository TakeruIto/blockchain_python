import os
import binascii

private_key = os.urandom(32)

print(private_key)
print(binascii.hexlify(private_key))