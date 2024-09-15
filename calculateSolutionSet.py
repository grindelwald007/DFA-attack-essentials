from binary_matrix import BinaryMatrix
from generateE1ImageSet import generateMapping as getE1
import numpy as np

def hex_to_binary_list(hex_string):
    integer_value = int(hex_string, 16)
    
    binary_string = bin(integer_value)[2:]
    
    binary_string = binary_string.zfill(len(hex_string) * 4)
    
    binary_list = [int(bit) for bit in binary_string]
    
    return binary_list

# a
matrix = np.array([
    [1, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 1, 1]
])

epsilon_in_hex = 'E7'

binary_matrix = BinaryMatrix(matrix)
epsilon = hex_to_binary_list(epsilon_in_hex)
c = 2

try:
    a_inverse = binary_matrix.find_inverse()
    res_1 = np.matmul(a_inverse, epsilon)
    # print(a_inverse)
    # print(epsilon)
    # print(res_1)
    
    res_2 = 2*res_1
    print(res_2)
    
    E1 = getE1()
    for e1 in E1:
        print(e1)
        res_3 = np.matmul(res_2,e1)
        print(res_3)

except ValueError as e:
    print(f"Error: {e}")
