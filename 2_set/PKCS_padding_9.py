
BLOCK_SIZE = 8
def plaintext_to_padded_bytes(plaintext, block_size=BLOCK_SIZE):
    missing =  -len(plaintext) % block_size
    padded = plaintext + missing*chr(missing)
    print(padded.encode())


if "__main__" == __name__:
    plaintext_to_padded_bytes("YELLOW SUBMARINE",20)
