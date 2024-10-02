import os, logging
import numpy as np
from constants import S_BOX as s_box, R_CON as rcon

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
        content = file.read().replace('[', '').replace(']', '').replace('\'', '').splitlines()
    
    data = [line.split() for line in content if line]
    hex_data = [[int(val, 16) for val in row] for row in data]

    array_2d = np.array(hex_data)
    
    array_1d_col_major = array_2d.flatten(order='F')
    
    return array_1d_col_major

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
    
    # i = Nb * (Nr+1) - Nk - 1
    
    while i >= 0:
        temp = w[i + Nk -1]
        
        if i % Nk == 0:
            # print(f"i {i} Nk+1 {Nk+1} i//(Nk+1) {i//Nk} rcon[] {hex(rcon[i//Nk])}")
            # print(f"i {i} Nk+1 {Nk+1} i//(Nk+1) {i//(Nk+1)} i//Nk+1 {i//Nk+1}")
            temp = xor_words(sub_word(rot_word(temp)), [rcon[i//Nk], 0x0, 0x0, 0x0])
        elif Nk > 6 and i % Nk == 4:
            temp = sub_word(temp)
            
        w[i] = xor_words(w[i + Nk], temp)
        i = i - 1
            
    return w




# Column major order
# final key = [ insert key ]

final_key = read_array_from_file("keys/Key_10.txt")
Nk = 4 
expanded_key = recover_key(final_key, Nk)

for i, word in enumerate(expanded_key):
    logging.debug(f"w[{i}]: " + ' '.join(f'{byte:02x}' for byte in word))
    
    
def int_to_ascii(val):
    try:
        return chr(val)
    except ValueError:
        return '?'

def traverse_column_major_and_convert_to_ascii(matrix):
    num_cols = len(matrix[0])
    num_rows = len(matrix)
    
    ascii_values = []
    
    for row in range(num_rows):
        for col in range(num_cols):
            hex_value = matrix[row][col]
            # ascii_char = int_to_ascii(hex_value)
            # ascii_values.append(ascii_char)
            ascii_values.append(hex(hex_value))
            
    
    return ascii_values


key_0_ascii = traverse_column_major_and_convert_to_ascii([expanded_key[0], expanded_key[1], expanded_key[2], expanded_key[3]])

logging.debug(f"AES-128 init key: {key_0_ascii}")

with open('keys/Key_1.txt', 'w') as file:
    file.write(str(key_0_ascii))