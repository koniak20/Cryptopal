from Crypto.Cipher import AES
from base64 import b64decode as b64d
from pwn import xor

BLOCK_SIZE = 16
key = b'YELLOW SUBMARINE'
iv = b'\x00'*BLOCK_SIZE
aes = AES.new(key,AES.MODE_ECB)

def CBC_encrypt(data):
    result = bytearray()
    parts = [data[i:i+BLOCK_SIZE] for i in range(0,len(data),BLOCK_SIZE)]
    previous = iv
    for curr in parts:
        curr = xor(previous,curr)
        curr = aes.decrypt(curr)
        previous = curr
        result += curr
    return result

def CBC_decrypt(data):
    result = bytearray()
    parts = [data[i:i+BLOCK_SIZE] for i in range(0,len(data),BLOCK_SIZE)]
    previous = iv
    for part in parts:
        curr = aes.decrypt(part)
        curr = xor(previous,curr)
        previous = part
        result += curr
    return result.decode()
    
with open("10.txt") as file:
    data = file.readlines()
data = "".join(data).rstrip()
print(CBC_decrypt(b64d(data.encode())))

