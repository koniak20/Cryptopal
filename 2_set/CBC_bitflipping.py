from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad,unpad
BLOCK_SIZE = 16
KEY = get_random_bytes(BLOCK_SIZE)
IV = get_random_bytes(BLOCK_SIZE)


def encryption(data: str) -> bytes:
    prefix = "comment1=cooking%20MCs;userdata="
    if any((char in data for char in ["=",";"])):
        print("You can't put '=' or ';' characters!\n")
        exit()
    sufix = ";comment2=%20like%20a%20pound%20of%20bacon"
    data = prefix + data + sufix
    data = pad(data.encode(),BLOCK_SIZE)
    aes = AES.new(KEY,AES.MODE_CBC,iv=IV)
    data = aes.encrypt(data)
    return data 

if "__main__" == __name__:
    print(len(encryption("-")))
