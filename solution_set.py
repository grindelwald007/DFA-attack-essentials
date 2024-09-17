from binary_matrix import BinaryMatrix
from e1_image_set import generate_mapping as get_e1, gf_mult as gf_mult, inverse_gf2m_field as gf_inverse
import numpy as np

A = np.array([
    [1, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 1, 1]
])

E1 = get_e1()

class MatrixOperations:
    def __init__(self):
        self.binary_matrix = BinaryMatrix(A)
        self.E1 = list(set(E1))
        self.E1.remove('0x0')
        print(sorted(self.E1))
        
    def hex_to_binary_list(self, hex_string):
        integer_value = int(hex_string, 16)
        binary_string = bin(integer_value)[2:]
        binary_string = binary_string.zfill(len(hex_string) * 4)
        binary_list = [int(bit) for bit in binary_string]
        return binary_list

    def compute_set(self, c, epsilon_hex):
        epsilon = self.hex_to_binary_list(epsilon_hex)
        
        try:
            # Find the inverse of the matrix
            a_inverse = self.binary_matrix.find_inverse()
            
            if self.binary_matrix.verify_inverse()[0]:
                
                raise ValueError("Error in A_INVERSE calculation")
            
            # Multiply the inverse matrix with epsilon
            res_1 = self.binary_matrix.custom_multiply(a_inverse, epsilon)
            
            # Convert the result to integer and hexadecimal
            res_1_int, _ = self.binary_matrix.bin_arr_to_hex(res_1)
            # print("(a_1*ε) in hex : ", _)
            # print("(a_1*ε) in int : ", res_1_int)
            
            # Perform the field multiplication
            res_2 = gf_mult(c, res_1_int)
            # print("c.(a_1*ε) gmul : ", res_2)``
            
            set_s = set()
            
            for e in self.E1:
                res_3 = gf_mult(int(e, 16), res_2)
                res_4 = gf_inverse(res_3)
                set_s.add(hex(res_4))
                # print(f"e : {e} | (c.(a_1*ε).e)_1 : {res_4}")
                
            return set_s

        except ValueError as e:
            print(f"Error: {e}")

# Example usage
# epsilon_in_hex = 'E7'
# c = 2

# operations = MatrixOperations()
# operations.computeSet(epsilon_in_hex, c)
