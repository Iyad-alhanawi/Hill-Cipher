import numpy as np
import string
from math import gcd

def get_key():
    """Function to get a 2x2 cipher key from user input."""
    cipher_key = []
    print("Enter your key in rows (4 integers):")
    for i in range(2):  # A for loop for row entries
        row = []
        for j in range(2):  # A for loop for column entries
            while True:
                try:
                    value = int(input(f"Key[{i+1}][{j+1}]: "))
                    row.append(value)
                    break
                except ValueError:
                    print("Please enter a valid integer.")
        cipher_key.append(row)
    return np.array(cipher_key)

def is_valid_key(cipher_key):
    """Check if the key is valid (determinant must be coprime to 26)."""
    det = int(np.round(np.linalg.det(cipher_key))) % 26
    return gcd(det, 26) == 1

def encrypt(plain_text, cipher_key):
    """Encrypts the plain text using the Hill cipher."""
    # Check if the key is valid
    if not is_valid_key(cipher_key):
        raise ValueError("Invalid key. The determinant must be coprime to 26.")

    # Remove spaces and convert to lowercase
    plain_text = plain_text.replace(" ", "").lower()
    
    # Convert plain text to numerical indices
    plain_index = [ord(char) - 97 for char in plain_text]
    
    # Pad with an extra character if the length is odd
    if len(plain_index) % 2 != 0:
        plain_index.append(ord('x') - 97)  # Padding with 'x'

    # Split plain index into pairs
    split = [plain_index[i:i+2] for i in range(0, len(plain_index), 2)]
    cipher_index = []

    for pair in split:
        c1 = (pair[0] * cipher_key[0][0] + pair[1] * cipher_key[0][1]) % 26
        c2 = (pair[0] * cipher_key[1][0] + pair[1] * cipher_key[1][1]) % 26
        cipher_index.extend([c1, c2])

    # Convert cipher index back to characters
    cipher_text = ''.join(chr(index + 97) for index in cipher_index)
    return cipher_text

def mod_inverse(a, m):
    """Computes the modular inverse of a under modulo m."""
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("Modular inverse does not exist.")

def decrypt(cipher_text, cipher_key):
    """Decrypts the cipher text using the Hill cipher."""
    # Convert cipher text to numerical indices
    cipher_index = [ord(char) - 97 for char in cipher_text if char != ' ']
    
    # Calculate determinant
    det = int(np.round(np.linalg.det(cipher_key)))
    det_mod = mod_inverse(det % 26, 26)  # Modular inverse of determinant

    # Calculate the inverse key
    inverse_cipher_key = np.array([[cipher_key[1][1], -cipher_key[0][1]],
                                    [-cipher_key[1][0], cipher_key[0][0]]])
    
    # Apply modular arithmetic
    inverse_cipher_key = (inverse_cipher_key * det_mod) % 26

    # Split cipher index into pairs
    split = [cipher_index[i:i+2] for i in range(0, len(cipher_index), 2)]
    plain_index = []

    for pair in split:
        p1 = (pair[0] * inverse_cipher_key[0][0] + pair[1] * inverse_cipher_key[0][1]) % 26
        p2 = (pair[0] * inverse_cipher_key[1][0] + pair[1] * inverse_cipher_key[1][1]) % 26
        plain_index.extend([p1, p2])

    # Convert plain index back to characters
    plain_text = ''.join(chr(index + 97) for index in plain_index)
    return plain_text

def main():
    while True:
        choice = input("Do you want to perform encryption or decryption? \n").lower()
        
        if choice == "encryption":
            plain_text = input("Enter your plain text: ")
            cipher_key = get_key()
            cipher_text = encrypt(plain_text, cipher_key)
            print(f"Cipher text: {cipher_text}")
            break  # Exit the loop after successful encryption

        elif choice == "decryption":
            cipher_text = input("Enter your cipher text: ")
            cipher_key = get_key()
            plain_text = decrypt(cipher_text, cipher_key)
            print(f"Plain text: {plain_text}")
            break  # Exit the loop after successful decryption

        else:
            print("Invalid choice. Please choose 'encryption' or 'decryption'.")
            
if __name__ == "__main__":
    main()
