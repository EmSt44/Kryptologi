import sys
import pickle
import time
from math import log
from itertools import product
from random import randrange

# Define the Swedish alphabet including å, ä, and ö
ALPHABET = "abcdefghijklmnopqrstuvwxyzåäö"
ALPHABET_SIZE = len(ALPHABET)

# Define the frequency table of the swedish alphabet, data taken from https://en.wikipedia.org/wiki/Letter_frequency
MONOFREQUENCIES = [0.09382, 0.01534, 0.01485, 0.04701, 0.10148, 0.02026, 0.02861, 0.02090, 0.05816, 0.00613, 0.03140, 0.05275, 0.03471, 0.08542, 0.04482, 0.01839, 0.00020, 0.08431, 0.06590, 0.07691, 0.01919, 0.02415, 0.00142, 0.00159, 0.00708, 0.00070, 0.01340, 0.01800, 0.01310]

# Frequency tetragram of swedish text
with open("tetrafrequencies.pkl", "rb") as f:
    TETRAFREQUENCIES = pickle.load(f)

# Cleans the text to not contain any other characters than the 29 alphabet letters
def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove all non-Swedish letters
    text = ''.join([char for char in text if char in ALPHABET])
    
    return text

def decrypt(ciphertext,key):
 plaintext = ''

 for i in range(len(ciphertext)):
     p = ALPHABET.index(ciphertext[i])
     k = ALPHABET.index(key[i%len(key)])
     c = (p - k) % 29
     plaintext += ALPHABET[c]

 return plaintext

# Find the fitness of a text by comparing tetrafrequency of known swedish text
# Testing with the same text ass the tetragram is derived from yields -9.6 and other swedish texts yield results in close proximity
def fitness(text):
    if len(text) < 4:
        return float('-inf')  # Too short to evaluate

    alphabet_dict = {ch: idx for idx, ch in enumerate(ALPHABET)}
    result = 0

    for i in range(len(text) - 3):
        tetragram = text[i:i+4]
        try:
            x = (alphabet_dict[tetragram[0]]*29**3 +
                 alphabet_dict[tetragram[1]]*29**2 +
                 alphabet_dict[tetragram[2]]*29 +
                 alphabet_dict[tetragram[3]])
            y = TETRAFREQUENCIES[x]
        except KeyError:
            y = 0  # If a character is not in the alphabet, assume it's very rare

        if y == 0:
            result += -1000  # Some large negative value, penalizes letter combinations that do not occur in swedish text
        else:
            result += log(y) # Make result logarithmic to avoid too small numbers, some rare tetragrams have very small frequencies

    return result / (len(text) - 3) # Normalize with the amount of tetragrams in the text to allow different lengths of text to be compared

# Find the index of coincidence for letters in a text 
def index_of_coincidence(text):
    counts = [0]*29

    for char in text: # Count the amount of times a letter appears in text
        counts[ALPHABET.index(char)] += 1
    freq = 0 # Frequency of a certain letter
    total = 0 # Total number of letters

    for i in range(29):
        freq += counts[i]*(counts[i]-1)
        total += counts[i]

    return 29*freq / (total*(total-1)) # Normalize by factor 29, this makes random text have an ioc of about 1

# Find the length of the key using the ioc formula
def find_key_length(text):
    found = False
    period = 0

    while not found:
        period += 1
        slices = ['']*period

        for i in range(len(text)):
            slices[i%period] += text[i]
        sum = 0

        for i in range(period):
            sum += index_of_coincidence(slices[i])
        ioc = sum / period

        if ioc > 1.6: # The ioc for a swedish text was tested to be around 1.7
            found = True

    return period

# Brute force crack a given ciphertext with a known key length by comparing texts decrypted with a certain key to the ioc
def brute_force(ciphertext, length):
    best_key = None
    best_fitness = float('-inf')
    
    # Generate all possible keys of given length using Swedish alphabet
    for key_tuple in product(ALPHABET, repeat=length):
        key = ''.join(key_tuple)
        decrypted_text = decrypt(ciphertext, key)
        score = fitness(decrypted_text)
        
        if score > best_fitness:
            best_fitness = score
            best_key = key
        
        if score > -50:  # Threshold for determining valid Swedish text
            break
    
    return best_key, decrypt(ciphertext, best_key) if best_key else None

# Randomly varies the key and updates it with the best found fitness until an acceptable fitness is found
def variational_key(ciphertext, length, fitness_threshold):
    key = ['a']*length # A starting key with all positions set to a
    best_fitness = -9999 # Start at a large negative number

    while best_fitness < fitness_threshold: # Threshold for determining valid swedish text
        k = key[:]
        random_index = randrange(length)

        for i in range(29): # select random index and run through the alphabet to find the best fitness
            k[random_index] = ALPHABET[i] 
            decrypted_text = decrypt(ciphertext, k)
            current_fitness = fitness(decrypted_text)

            if (current_fitness > best_fitness):
                key = k[:]
                best_fitness = current_fitness

    return "".join(key), decrypt(ciphertext, key)




def main():
    if len(sys.argv) != 2:
        print("Usage: python3 vigenereSolver.py <input_file>")
        return
    
    input_file = sys.argv[1]

    file_path = input_file
    with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    
    # START TIMING #
    start_time = time.time() # For recording time to solve

    key_length = find_key_length(text)
    print("key length is:", key_length)
    if (key_length > 4):
        key, decrypted_text = variational_key(text, key_length, -100)
    else:
        key, decrypted_text = brute_force(text, key_length)

    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time  # Compute elapsed time
    # STOP TIMING #

    print("The key is:", key)
    print("Decrypted text:")
    print(decrypted_text)
    print("Time to crack:", elapsed_time)
   

if __name__ == "__main__":
    main()
