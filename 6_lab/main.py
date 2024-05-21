import math
from bitarray import bitarray

class HuffmanTree:
    def __init__(self, label=None, prob=0, left=None, right=None):
        self.left = left
        self.right = right
        self.label = label
        self.prob = prob

def open_file(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()

def count_chars(text, offset):
    count = {}
    for i in range(len(text) - offset + 1):
        count[text[i:i + offset]] = count.get(text[i:i + offset], 0) + 1
    total = sum(count.values())
    for key in count.keys():
        count[key] /= total
    return sorted(count.items(), key=lambda t: t[1])

def build_HuffmanTree(list):
    HuffmanTree_list = [HuffmanTree(el[0], el[1]) for el in list]
    HuffmanTree_list.append(HuffmanTree('EOF', 0.0))
    HuffmanTree_list = sorted(HuffmanTree_list, key=lambda HuffmanTree: HuffmanTree.prob)
    while len(HuffmanTree_list) > 1:
        t1 = HuffmanTree_list.pop(0)
        t2 = HuffmanTree_list.pop(0)
        new_HuffmanTree = HuffmanTree(t1.label + t2.label, t1.prob + t2.prob, t1, t2)
        HuffmanTree_list.append(new_HuffmanTree)
        HuffmanTree_list = sorted(HuffmanTree_list, key=lambda HuffmanTree: HuffmanTree.prob)
    return HuffmanTree_list[0]

def generate_codes(HuffmanTree, codes, bits=''):
    if HuffmanTree.left is None and HuffmanTree.right is None:
        codes[HuffmanTree.label] = bits
    else:
        generate_codes(HuffmanTree.left, codes, bits + '0')
        generate_codes(HuffmanTree.right, codes, bits + '1')

def length_and_efficiency(codes, list):
    legth = 0.0
    entropy = 0.0
    for el in list:
        legth += float(el[1]) * float(len(codes[el[0]]))
        entropy += el[1] * math.log2(el[1])
    return (legth, -entropy / legth)

def create(text):
    list = count_chars(text, 1)
    HuffmanTree = build_HuffmanTree(list)
    code = {}
    generate_codes(HuffmanTree, code)
    avg_len, eff = length_and_efficiency(code, list)
    print(f"Średnia długość kodu: {round(avg_len, 2)}")
    print(f"Efektywność kodowania: {round(eff * 100, 2)}%")
    return code

def encode(text, code):
    bits = bitarray()
    for char in text:
        bits += bitarray(code[char])
    bits += code['EOF']
    return bits

def decode(bits, code):
    decoded = []
    decoded_map = {v: k for k, v in code.items()}
    temp = []
    for bit in bits:
        temp.append(str(bit))
        if ''.join(temp) in decoded_map:
            char = decoded_map[''.join(temp)]
            if char == 'EOF':
                break
            decoded.append(char)
            temp = []
    return ''.join(decoded)

def save(encoded, codes):
    with open("code.txt", "w") as file:
        for key, val in codes.items():
            file.write(f"{key},{val}\n")
    with open("encoded.bin", "wb") as file:
        file.write(encoded)

def load():
    with open("code.txt", "r") as file:
        lines = file.readlines()
    codes = {line.split(",")[0]: line.split(",")[1].strip() for line in lines}
    bits = bitarray()
    with open("encoded.bin", "rb") as file:
        bits.frombytes(file.read())
    return bits, codes

def compare_texts(original, decoded):
    return "Tekst oryginalny i zakodowany-odkodowany są identyczne" if original == decoded else "Tekst oryginalny i zakodowany-odkodowany nie są identyczne"

def main():
    text = open_file("norm_wiki_sample.txt")
    code = create(text)
    encoded = encode(text, code)
    save(encoded, code)
    loaded_encoded, loaded_codes = load()
    decoded = decode(loaded_encoded, loaded_codes)
    print(compare_texts(text, decoded))

if __name__ == '__main__':
    main()
