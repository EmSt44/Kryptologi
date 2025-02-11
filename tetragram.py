import pickle

# Define Swedish alphabet
ALPHABET = "abcdefghijklmnopqrstuvwxyzåäö"
ALPHABET_SIZE = len(ALPHABET)

def tetrafrequencies(text):
    freq_size = ALPHABET_SIZE ** 4
    tetra_freq = [0] * freq_size
    
    for i in range(len(text) - 3):
        x = (ALPHABET.index(text[i]) * ALPHABET_SIZE ** 3 +
             ALPHABET.index(text[i+1]) * ALPHABET_SIZE ** 2 +
             ALPHABET.index(text[i+2]) * ALPHABET_SIZE +
             ALPHABET.index(text[i+3]))
        tetra_freq[x] += 1
    
    total = len(text) - 3
    if total > 0:
        tetra_freq = [count / total for count in tetra_freq]
    
    return tetra_freq

def main():
    with open("compiled_output.txt", "r", encoding="utf-8") as f:
        text = f.read().lower()
        text = ''.join([c for c in text if c in ALPHABET])
    
    tetra_freq = tetrafrequencies(text)
    
    with open("tetrafrequencies.pkl", "wb") as tetrafile:
        pickle.dump(tetra_freq, tetrafile)
    
    print("Tetrafrequencies saved to file")

if __name__ == "__main__":
    main()

