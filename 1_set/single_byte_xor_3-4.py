import sys

freq = { ' ' : 1, 'e' : 1.3, 'E': 1.3, 'T' : 0.91, 't' : 0.91, 'A' : 0.82, 'a' : 0.82, 'O' : 0.75, 'o': 0.75, 'I' : 0.7, 'i': 0.7, 'N' : 0.67, 'n':0.67,'S' : 0.63, 's': 0.63, 'H' : 0.61, 'h': 0.61, 'R' : 0.6, 'r': 0.6, 'D' : 0.43, 'd':0.43,'L' : 0.4 , 'l': 0.4 ,'C' : 0.28 , 'c': 0.28 ,'U' : 0.28 , 'u': 0.28 ,'M' : 0.24 , 'm': 0.24 ,'W' : 0.24 , 'w': 0.24 , 'F' : 0.22 , 'f': 0.22 ,'G' : 0.2 , 'g': 0.2 ,'Y' : 0.2 , 'y': 0.2, 'P' : 0.19 , 'p': 0.19, 'B' : 0.15, 'b':0.15, 'V' : 0.098, 'v' : 0.098, 'K' : 0.077, 'k' : 0.077, 'X' : 0.015, 'J': 0.015}
alphabet = 'ABCDEFGHIJKLMNOPRSTUVWXY '

def scoring(text):
    score = 0
    text = text.upper()
    length = len(text)
    if length == 0:
        return 0
    for letter in alphabet:
        score += round(10*freq[letter] *(text.count(letter)/length),3)
    return round(score,2)

if __name__ == "__main__":
    texts = []
    if len(sys.argv) == 2:
        text = ""
        with open(sys.argv[1]) as file:
            lines = file.readlines()
            for line in lines:
                texts.append(bytes.fromhex(line.rstrip()))
    else:
        text = bytes.fromhex("73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d")
    if len(texts) == 0:
        texts.append(text)
    end_result = []
    for text in texts:
        best_score = 0
        new = bytearray(len(text))
        result = ""
        for i in range(256):
            for j,a in enumerate(text):
                new[j] = a ^ i
            new_score = scoring(new.decode(errors="ignore"))
            if new_score > best_score:
                best_score = new_score
                result = new.decode(errors="ignore")
        end_result.append((best_score,len(result),result))
    end_result.sort()
    for score,length,result in end_result:
        print(f"{score} {length} {result}")
