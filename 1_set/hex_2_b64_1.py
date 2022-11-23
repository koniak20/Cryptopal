import base64

def hex_2_base64(text):
    return base64.b64encode(bytes.fromhex(text)).decode()
def base64_2_hex(text):
    return base64.b64decode(text.encode()).hex()

result = hex_2_base64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d")
print(base64_2_hex(result))
