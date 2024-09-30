import os, logging
import numpy as np
from constants import S_BOX as s_box

log_folder = 'logs'

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file = os.path.join(log_folder, 'recovery.log')

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def read_array_from_file(filename):
    with open(filename, 'r') as file:
        # Read the content and remove unwanted characters
        content = file.read().replace('[', '').replace(']', '').replace('\'', '').splitlines()
    
    # Split each row and create a list of lists (2D array)
    data = [line.split() for line in content if line]
    
    # Convert the hex strings to integers if needed (can also keep them as hex strings)
    hex_data = [[int(val, 16) for val in row] for row in data]

    # Convert it to a NumPy array
    array_2d = np.array(hex_data)
    
    # Convert the array to column-major order 1D array (Fortran-like order)
    array_1d_col_major = array_2d.flatten(order='F')
    
    return array_1d_col_major

# Rcon table for AES
rcon = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36
]

"""Apply the S-Box substitution to a 4-byte word."""
def sub_word(word):
    return [s_box[b] for b in word]

"""Rotate the 4-byte word left (circular shift)."""
def rot_word(word):
    return word[1:] + word[:1]

"""XOR two 4-byte words."""
def xor_words(word1, word2):

    return [b1 ^ b2 for b1, b2 in zip(word1, word2)]

def recover_key(final_key, Nk=4):
    Nb = 4  # Block size in words for AES (fixed as 4)
    Nr = 10  # Number of rounds for AES-128 (Nk=4, Nr=10)

    w = [[0, 0, 0, 0] for _ in range(Nb * (Nr + 1))] 
    
    i = Nb * (Nr+1) - 1
    j = Nk - 1
    
    while j >= 0:
        w[i] = [final_key[4*j], final_key[4*j + 1], final_key[4*j + 2], final_key[4*j + 3]]
        i = i - 1
        j = j - 1
    
    i = Nb * (Nr+1) - Nk - 1
    
    while i >= 0:
        temp = w[i + Nk -1]
        
        if i % Nk == 0:
            temp = xor_words(sub_word(rot_word(temp)), [rcon[i//(Nk+1)], 0x0, 0x0, 0x0])
        elif Nk > 6 and i % Nk == 4:
            temp = sub_word(temp)
            
        w[i] = xor_words(w[i + Nk], temp)
        i = i - 1
            
    return w




# Column major order
# final_key = [0xd0, 0x14, 0xf9, 0xa8, 0xc9, 0xee, 0x25, 0x89, 0xe1, 0x3f, 0x0c, 0xc8, 0xb6, 0x63, 0x0c, 0xa6]



final_key = read_array_from_file("Key_10.txt")
Nk = 4 
expanded_key = recover_key(final_key, Nk)

for i, word in enumerate(expanded_key):
    logging.debug(f"w[{i}]: " + ' '.join(f'{byte:02x}' for byte in word))

