from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad,unpad
from base64 import b64decode
from random import randint
from collections import Counter

BLOCK_SIZE = 16
RAND_KEY = get_random_bytes(BLOCK_SIZE)
ASCII_RANGE = (0,128)
PREFIX_SIZE = randint(1,20)
PREFIX = get_random_bytes(PREFIX_SIZE)
SUFIX = b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")


# AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)

def prependData(inputData: str, key: bytes = RAND_KEY) -> bytes:
    plaintext = PREFIX + inputData.encode() + SUFIX
    plaintext = pad(plaintext, BLOCK_SIZE)
    aes = AES.new(key,AES.MODE_ECB)
    ciphertext = aes.encrypt(plaintext)
    return ciphertext

def detectCBC_ECB(function):
    payload = "A" * (BLOCK_SIZE*3)
    data = function(payload)
    blocks = [ data[BLOCK_SIZE*i:BLOCK_SIZE*(i+1)] for i in range(len(data)//BLOCK_SIZE) ]
    values = Counter(blocks).values()
    if 2 in values or 3 in values:
        return "ECB"
    return "Not ECB"

def findSize(encryption) -> int:
    begin = len(encryption("",RAND_KEY))
    new = begin
    count = 0
    while begin == new:
        count += 1
        new = len(encryption("A"*count,RAND_KEY))
    
    prefix_sufix_len = begin - count  
    count_1 = -1
    while True:
        count_1 += 1
        count_2 = count - count_1
        new = encryption("A"*count_1 + "B"*2*BLOCK_SIZE + "A"*count_2, RAND_KEY)
        blocks = [ new[BLOCK_SIZE*i:BLOCK_SIZE*(i+1)] for i in range(len(new)//16) ]
        if 2 in Counter(blocks).values():
            previous = ""
            for i,block in enumerate(blocks):
                if previous == block:
                    prefix_size = BLOCK_SIZE*(i-1) - count_1
                    sufix_size = prefix_sufix_len - prefix_size
                    return (prefix_size,sufix_size)
                previous = block
        if count_1 == 1000:
            print("Something went wrong")
            exit()

def decryptECB(encryption):
    prefix_size,message_size = findSize(encryption)
    plaintext = ""
    garbage = BLOCK_SIZE - prefix_size%BLOCK_SIZE
    garbage_blocks = (prefix_size + garbage)//BLOCK_SIZE
    block = garbage_blocks - 1
    garbage = "A"*garbage
    while len(plaintext) != message_size:
        block += 1
        for i in range(BLOCK_SIZE-1,-1,-1):
            if len(plaintext) == message_size:
                break
            payload = i * "A"
            find = encryption(garbage + payload)[BLOCK_SIZE * block:BLOCK_SIZE*(block+1)]
            prefix = (garbage + payload + plaintext)[-(BLOCK_SIZE-1)::]
            options = {}
            long_text = garbage + "".join([ prefix + chr(j) for j in range(ASCII_RANGE[0],ASCII_RANGE[1])])
            all_options = encryption(long_text)
            for index,j in enumerate(range(ASCII_RANGE[0],ASCII_RANGE[1]),garbage_blocks):
                options[all_options[index*BLOCK_SIZE:(index+1)*BLOCK_SIZE:]] = chr(j)
            try:
                plaintext += options[find]
            except:
                print("Could not find letter!!!")
                print(f"All I could find is:\n{plaintext}\n\nMissing characters:{message_size-len(plaintext)}")
                exit() 
    return plaintext

if "__main__" == __name__:
    if detectCBC_ECB(prependData) != "ECB":
        print("This aes function don't use ECB")
        exit()
    plaintext = decryptECB(prependData)
    print(f"I found your plaintext:\n{plaintext}\nlen: {len(plaintext)}")

