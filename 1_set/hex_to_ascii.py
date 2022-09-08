
def hex_2_ascii(text):
    return bytes.fromhex(text).decode()

print(hex_2_ascii("e4c8c8cccec9c087eae480d487cbceccc287c687d7c8d2c9c387c8c187c5c6c4c8c9"))
