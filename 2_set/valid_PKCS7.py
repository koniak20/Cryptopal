

BLOCK_SIZE = 16

def unpad(data: bytes) -> bytes:
    pad_value = 0 
    for i,byte in enumerate(data[-BLOCK_SIZE:]):
        if pad_value > 0 and byte != pad_value:
            raise ValueError
        if pad_value == 0 and byte < BLOCK_SIZE:
            pad_value = BLOCK_SIZE - i
    return data[:-pad_value]

if "__main__" == __name__:
    text = b"ICE ICE BABY\x05\x03\x04\x04"
    print(unpad(text))
