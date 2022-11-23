from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad,unpad
from base64 import b64decode

BLOCK_SIZE = 16
RAND_KEY = get_random_bytes(BLOCK_SIZE)
ASCII_RANGE = (0,128)
# AES-128-ECB(attacker-controlled || target-bytes, random-key)

def prependData(inputData: str, key: bytes = RAND_KEY) -> bytes:
    sufix = b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
    plaintext = inputData.encode() + sufix
    plaintext = pad(plaintext, BLOCK_SIZE)
    aes = AES.new(key,AES.MODE_ECB)
    ciphertext = aes.encrypt(plaintext)
    return ciphertext

def detectCBC_ECB(function):
    payload = "A" * (BLOCK_SIZE*3)
    data = function(payload)
    if data[BLOCK_SIZE:BLOCK_SIZE*2] == data[BLOCK_SIZE*2:BLOCK_SIZE*3]:
        return "ECB"
    return "Not ECB"

def findMessageSize(encryption) -> int:
    begin = len(encryption("",RAND_KEY))
    new = begin
    count = 0
    while begin == new:
        count += 1
        new = len(encryption("A"*count,RAND_KEY))
    return  begin - count
def decryptECB(encryption):
    message_size = findMessageSize(encryption)
    plaintext = ""
    block = -1
    while len(plaintext) != message_size:
        block += 1
        for i in range(BLOCK_SIZE-1,-1,-1):
            if len(plaintext) == message_size:
                break
            payload = i * "A"
            find = encryption(payload)[BLOCK_SIZE * block:BLOCK_SIZE*(block+1)]
            prefix = (payload + plaintext)[-(BLOCK_SIZE-1)::]
            options = {}
            long_text = "".join([ prefix + chr(j) for j in range(ASCII_RANGE[0],ASCII_RANGE[1])])
            all_options = encryption(long_text)    
            for index,j in enumerate(range(ASCII_RANGE[0],ASCII_RANGE[1])):
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

