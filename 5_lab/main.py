from bitarray import bitarray

def open_file(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()

def count_chars(text):
    count = {}
    for char in text:
        count[char] = count.get(char, 0) + 1
    return sorted(count.items(), key=lambda item: item[1], reverse=True)

def create(text):
    list = count_chars(text)
    code = {char: f"{i:06b}" for i, (char, _) in enumerate(list)}
    code['EOF'] = f"{len(list):06b}"
    return code

def encode(text, code):
    bits = bitarray()
    for char in text:
        bits += bitarray(code[char])
    bits += bitarray(code['EOF'])
    return bits

def decode(bits, code):
    decoded = []
    decode_map = {v: k for k, v in code.items()}
    for i in range(0, len(bits), 6):
        symbol = decode_map[bits[i:i + 6].to01()]
        if symbol == 'EOF':
            break
        decoded.append(symbol)
    return ''.join(decoded)

def save(encoded, code):
    with open("code.txt", "w") as file:
        for char, bits in code.items():
            file.write(f"{char},{bits}\n")
    with open("encoded.bin", "wb") as file:
        file.write(encoded)

def load():
    with open("code.txt", "r") as file:
        code = {line.split(',')[0]: line.strip().split(',')[1] for line in file}
    encoded = bitarray()
    with open("encoded.bin", "rb") as file:
        encoded.frombytes(file.read())
    return encoded, code

def compare_texts(original, decoded):
    return "Tekst oryginalny i zakodowany-odkodowany są identyczne" if original == decoded else "Tekst oryginalny i zakodowany-odkodowany nie są identyczne"

def main():
    text = open_file("norm_wiki_sample.txt")
    code = create(text)
    encoded = encode(text, code)
    save(encoded, code)
    loaded_encoded, loaded_code = load()
    decoded = decode(loaded_encoded, loaded_code)
    print(compare_texts(text, decoded))

if __name__ == '__main__':
    main()
