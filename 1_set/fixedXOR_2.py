

def xor(a,b):
    result = ""
    for x,y in list(zip(a,b)):
        result += hex(int(x,base=16)^int(y,base=16))[-1]
    return result

if "746865206b696420646f6e277420706c6179" == xor("1c0111001f010100061a024b53535009181c","686974207468652062756c6c277320657965"):
    print("[True]")

result = ""
a = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
for i in a:
    result += hex(int(i,base=16) ^ 95)[-1]
print(result)

