
def xor(a,key):
    result = bytearray(len(a))
    for i, a in enumerate(a):
        result[i] = a ^ key[i % len(key)]
    return result.hex()
if __name__ == "__main__":
    text = "Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"
    print(xor(text.encode(),b'ICE')) 
