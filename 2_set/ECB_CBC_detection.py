from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from random import randint 

BLOCK_SIZE = 16

def randCBC_ECB(data):
    if type(data) == str:
        data = data.encode()
    key = get_random_bytes(BLOCK_SIZE)
    iv = get_random_bytes(BLOCK_SIZE)
    ECB = randint(0,1)
    prefix = bytearray([randint(0,255) for _ in range(randint(5,10))])
    sufix = bytearray([randint(0,255) for _ in range(randint(5,10))])
    data = prefix + data + sufix
    data = pad(data,BLOCK_SIZE)
    if ECB:
        aes = AES.new(key,AES.MODE_ECB)
    else:
        aes = AES.new(key,AES.MODE_CBC,iv=iv)
    data = aes.encrypt(data)
    return ECB,data # ECB to tell which mode was used

def detectCBC_ECB(function):
    payload = b'A' * (BLOCK_SIZE*3)
    answer,data = function(payload)
    ECB = 0
    # If second and third block are the same function used ECB
    if data[BLOCK_SIZE:BLOCK_SIZE*2] == data[BLOCK_SIZE*2:BLOCK_SIZE*3]:
        ECB = 1
    if ECB == answer:
        print("Good answer!")
        return 1
    else:
        print("wrong")
        return 0

    
if "__main__" == __name__:
    result = 0
    for _ in range(9000):
        result += detectCBC_ECB(randCBC_ECB)
    print(result)

