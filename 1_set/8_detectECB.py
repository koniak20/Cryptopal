
def unique(data):
    for n in data:
        if data.count(n)>1:
            return 0
    return 1
if "__main__" == __name__:
    with open("8.txt") as file:
        lines = file.readlines()
    data = [] 
    for line in lines:
        blocks = []
        line = line.rstrip()
        for i in range(0,len(line),32):
            blocks.append(line[i:i+32])
        if len(blocks):
            data.append(blocks)
    for ciphertext in data:
        if not unique(ciphertext):
            print("This was probably encrypted using ECB!\n","".join(ciphertext))
            print(ciphertext)
