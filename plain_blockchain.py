import hashlib
import datetime
from threading import main_thread
import time
import json
from tkinter.tix import MAIN
from unicodedata import name

INITIAL_BITS = 0x1d777777
MAX_32BIT = 0xffffffff

class Block():
    def __init__(self, index, prev_hash, data, timestamp, bits):
        self.index = index
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = 0
        self.elapsed_time = ""
        self.block_hash = ""

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def to_json(self):
        return {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "stored_data": self.data,
            "timestamp": self.timestamp.strftime("%Y/%m/%d %H:%M:%S"),
            "bits": hex(self.bits)[2:].rjust(8, "0"),
            "nonce": hex(self.nonce)[2:].rjust(8, "0"),
            "elapsed_time": self.elapsed_time,
            "block_hash": self.block_hash
        }

    def calc_blockhash(self):
        blockheader = str(self.index) + str(self.prev_hash) + str(self.data) + str(self.timestamp) + hex(self.bits)[2:] + str(self.nonce)
        h = hashlib.sha256(blockheader.encode()).hexdigest()
        self.block_hash = h
        return h

    def calc_target(self):
        exponent_bytes = (self.bits >> 24) - 3
        exponent_bits = exponent_bytes*8
        coefficient = self.bits & 0xffffff
        return coefficient << exponent_bits

    def check_valid_hash(self):
        return int(self.calc_blockhash(), 16) <= self.calc_target()

class Blockchain():
    def __init__(self, initial_bits):
        self.chain = []
        self.initial_bits = initial_bits

    def add_block(self, block):
        self.chain.append(block)

    def getblockinfo(self, index=-1):
        return print(json.dumps(self.chain[index].to_json(), indent=2, sort_keys=True, ensure_ascii=False))

    def mining(self, block):
        start_time = int(time.time() * 1000)
        while True:
            for n in range(MAX_32BIT + 1):
                block.nonce = n
                if block.check_valid_hash():
                    end_time = int(time.time() * 1000)
                    block.elapsed_time = str((end_time - start_time)/1000.) + "秒"
                    self.add_block(block)
                    self.getblockinfo()
                    return

            new_time = datetime.datetime.now()
            if new_time == block.timestamp:
                block.timestamp += datetime.timedelta(seconds=1)
            else:
                block.timestamp = new_time

    def create_genesis(self):
        genesis_block = Block(0, "0000000000000000000000000000000000000000000000000000000000000000", "ジェネシスブロック", datetime.datetime.now(), self.initial_bits)
        self.mining(genesis_block)

    def add_newblock(self, i):
        last_block = self.chain[-1]
        block = Block(i+1, last_block.block_hash, "ブロック "+str(i+1), datetime.datetime.now(), last_block.bits)
        self.mining(block)

if __name__=="__main__":
    bc = Blockchain(INITIAL_BITS)
    print("ジェネシスブロックを作成中・・・")
    bc.create_genesis()
    for i in range(30):
        print(str(i+2)+"番目のブロックを作成中・・・")
        bc.add_newblock(i)



