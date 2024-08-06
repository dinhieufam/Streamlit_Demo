import streamlit as st


def min_distance(a, b, c):
    if a <= b and a <= c:
        return a
    elif b <= c and b <= a:
        return b
    else:
        return c


def levenshtein_distance(a, b):
    distances = [[0]*(len(b) + 1) for _ in range((len(a) + 1))]

    for i in range(len(a)+1):
        distances[i][0] = i

    for i in range(len(b)+1):
        distances[0][i] = i

    for i in range(1, len(a)+1):
        for j in range(1, len(b)+1):
            if a[i-1] == b[j-1]:
                distances[i][j] = distances[i-1][j-1]
            else:
                distances[i][j] = min_distance(
                    distances[i-1][j], distances[i-1][j-1], distances[i][j-1]) + 1

    return distances[-1][-1]


def load_vocal(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    words = sorted(set([line.strip().lower() for line in lines]))

    return words


vocabs = load_vocal(file_path='./source/vocab.txt')

st.title('Word Correction')
word = st.text_input("Your Word")

if st.button("Compute"):
    distances = dict()

    for vocab in vocabs:
        distance = levenshtein_distance(word, vocab)
        distances[vocab] = distance

    sorted_distances = dict(
        sorted(distances.items(), key=lambda item: item[1]))

    correct_word = list(sorted_distances.keys())[0]

    st.write('Correct: ', correct_word)

    col1, col2 = st.columns(2)

    col1.write(vocabs)
    col2.write(sorted_distances)
