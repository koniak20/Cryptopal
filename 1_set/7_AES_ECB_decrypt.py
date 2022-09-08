from Crypto.Cipher import AES
import base64

key = b"YELLOW SUBMARINE"
aes = AES.new(key,AES.MODE_ECB)

def b64_hex(text):
    return base64.b64decode(text.encode())

with open("7.txt") as file:
    text = file.readlines()
data = "".join(text).rstrip()
data = b64_hex(data)
data = aes.decrypt(data)
print(data.decode())
