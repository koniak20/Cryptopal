from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad,unpad

BLOCK_SIZE = 16
KEY = get_random_bytes(BLOCK_SIZE)

def parse(data: str) -> dict:
    data = data.split("&")
    result = {}
    try:
        for arg in data:
            first,second = arg.split("=")
            result[first] = second
    except:
        print("Something went wrong!")
        exit()
    return result

NEXT_UID = 10
def profile_for(email: str) -> dict:
    global NEXT_UID
    if "&" in email or "=" in email:
        print("In your email can not be & or =!")
        exit()
    cookie = f"email={email}&uid={NEXT_UID}&role=user"
    NEXT_UID += 1
    aes = AES.new(KEY,AES.MODE_ECB)
    return aes.encrypt(pad(cookie.encode(),BLOCK_SIZE))

def decrypt_profile(ciphertext: bytes) -> dict:
    aes = AES.new(KEY,AES.MODE_ECB)
    decrypted = aes.decrypt(ciphertext)
    cookie = unpad(decrypted,BLOCK_SIZE).decode()
    return parse(cookie)

if __name__ == "__main__":
    email = "myemail@wp.pl"
    normal_cookie = profile_for(email)
    payload = b"AAAAAAAAAAadmin" + (b"\x0b"*11) + b"@wp.pl"
    admin = profile_for(payload.decode())[BLOCK_SIZE:2*BLOCK_SIZE]
    admin_cookie = normal_cookie[:2*BLOCK_SIZE] + admin
    # 6 + 10 + 3 + 13 dwa pierwsze bloki
    # 6 + 10 + "admin" + "0x0b"* 11 
    print(decrypt_profile(admin_cookie))

    
