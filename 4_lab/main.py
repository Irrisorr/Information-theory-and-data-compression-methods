import math
import numpy as np


def open_file(filename):
    with open(file=filename, encoding='utf-8') as file:
        return file.read()


def prob_words_with_lett(text, offset = 1):
    prob = {}
    for i in range(len(text) - offset + 1):
        prob[tuple(text[i:i + offset])] = prob.get(tuple(text[i:i + offset]),0) + 1
    sumOfKeys = sum(list(prob.values()))

    for propability in prob.keys():
        prob[propability] /= sumOfKeys

    return prob


def calculate_entropy(prob):
    entropy = 0.0
    for key in prob.keys():
        entropy += prob[key] * math.log2(prob[key])

    return -entropy


def calculate_conditional_entropy(prob_sec, prob_first):
    con_entropy = 0.0
    for key in prob_sec.keys():
        con_probabliity = prob_sec[key] / prob_first[key[:-1]]
        con_entropy += prob_sec[key]  * math.log2(con_probabliity)
    
    return -con_entropy


def calculate_chars_entropies(text):
    output_list = []
    probabilities = prob_words_with_lett(text) 
    output_list.append(calculate_entropy(probabilities))
    for i in [1,2,3,4,5]:
        tmp_prob = prob_words_with_lett(text, i+1)
        output_list.append(calculate_conditional_entropy(tmp_prob, probabilities))
        probabilities = tmp_prob
    
    return output_list


def calculate_words_entropies(words):
    output_list = []
    probabilities = prob_words_with_lett(words) 
    output_list.append(calculate_entropy(probabilities))

    for i in [1,2,3,4,5]:
        tmp_prob = prob_words_with_lett(words, i+1)
        output_list.append(calculate_conditional_entropy(tmp_prob, probabilities))
        probabilities = tmp_prob

    return output_list


def generate(file):
    text = open_file(filename=file)
    chars_entropies_list = calculate_chars_entropies(text)

    print("Chars entropies:")
    for i in range(len(chars_entropies_list)):
        if i == 0:
            print("Entropy: " + str(chars_entropies_list[i]))
        else:
            print(str(i) + " conditional entropy: " + str(chars_entropies_list[i]))

    words_entropies_list = calculate_words_entropies(list(text.split()))
    for i in range(len(words_entropies_list)):
        if i == 0:
            print("Entropy: " + str(words_entropies_list[i]))
        else:
            print(str(i) + " conditional entropy: " + str(words_entropies_list[i]))

    return [chars_entropies_list[1:], words_entropies_list[1:]]


def check(sample_entropies, chars_min_max, words_min_max):
    counter = 0
    for i in range(len(sample_entropies[0])):

        if sample_entropies[0][i] >= chars_min_max[i][0] and sample_entropies[0][i] <= chars_min_max[i][1]:
            counter += 1
        if sample_entropies[1][i] >= words_min_max[i][0] and sample_entropies[1][i] <= words_min_max[i][1]:
            counter += 1
    
    if counter >= len(sample_entropies[0]):
        return "Yes"
    else:
        return "No"


def main():
    matrix_entropies_chars = []
    matrix_entropies_words = []

    filenames = ["norm_wiki_en.txt", "norm_wiki_la.txt", "norm_wiki_eo.txt", "norm_wiki_et.txt", "norm_wiki_ht.txt", "norm_wiki_nv.txt", "norm_wiki_so.txt"]
    for file in filenames:
        print("Entropies for file: " + file)
        result = generate(file)
        matrix_entropies_chars.append(result[0])
        matrix_entropies_words.append(result[1])
    chars_min_max = []
    words_min_max = []
    matrix_entropies_chars = np.transpose(matrix_entropies_chars)
    matrix_entropies_words = np.transpose(matrix_entropies_words)

    for i in range(5):
        chars_min_max.append([min(matrix_entropies_chars[i]), max(matrix_entropies_chars[i])])
        words_min_max.append([min(matrix_entropies_words[i]), max(matrix_entropies_words[i])])

    print("\n==============TASK 'Is it a language?'=============='\n")
    sample_names = ["sample0.txt", "sample1.txt", "sample2.txt", "sample3.txt", "sample4.txt", "sample5.txt"]
    for file in sample_names:
        print("Entropies for file: " + file)
        result = generate(file)
        print()
        print("Is it a language?: " + file + ": " + str(check(result, chars_min_max, words_min_max)))
        print()


if __name__  == '__main__':
    main()