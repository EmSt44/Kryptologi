import sys

# Define the Swedish alphabet including å, ä, and ö
ALPHABET = "abcdefghijklmnopqrstuvwxyzåäö"
ALPHABET_SIZE = len(ALPHABET)

def read_file(filename):
    """Reads a file and returns its content as a stripped string."""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().strip()

def vigenere_cipher(text, key, encrypt):
    """Encrypts or decrypts a given text using the Vigenère cipher, removing whitespaces when encrypting."""
    encrypt = True #True to encrypt, False to decrypt
    result = []
    key_length = len(key)
    key_indices = [ALPHABET.index(k) for k in key]
    key_pos = 0

    if encrypt:
        print("Encrypting")
    else:
        print("Decrypting")
    
    for char in text:
        if char == ' ' and encrypt:
            continue
        
        text_index = ALPHABET.index(char)
        key_index = key_indices[key_pos % key_length]
        
        if encrypt:
            new_index = (text_index + key_index) % ALPHABET_SIZE
        else:
            new_index = (text_index - key_index) % ALPHABET_SIZE
        
        result.append(ALPHABET[new_index])
        key_pos += 1
    
    return ''.join(result)

def main():
    if len(sys.argv) != 4:
        print("Usage: python vigenere.py <input_file> <key_file> <output_file>")
        return
    
    input_file, key_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]
    plaintext = read_file(input_file)
    key = read_file(key_file)
    
    ciphertext = vigenere_cipher(plaintext, key, encrypt=True)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(ciphertext)
    
    print(f"Encrypted text written to {output_file}")

if __name__ == "__main__":
    main()
