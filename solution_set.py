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

A_INV = np.array([
    [0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0]
])

E1 = get_e1()[0]

class MatrixOperations:
    def __init__(self):
        self.binary_matrix = BinaryMatrix(A)
        self.E1 = list(set(E1))
        self.E1.remove('0x0')
        # print(sorted([int(_, 16) for _ in self.E1]))
    
    def get_e1_star_list(self):
        return self.E1
    
    @staticmethod
    def hex_to_binary_list(hex_string):
        integer_value = int(hex_string, 16)
        if integer_value < 0 or integer_value > 255:
            raise ValueError("Value outside GF(2^8) field")

        binary_string = bin(integer_value)[2:].zfill(8)
        binary_list = [int(bit) for bit in binary_string]
        return binary_list


    def compute_set(self, c, epsilon_prime_hex):
        # reversing is done . See epsilon_calculator.py
        epsilon_prime_hex = epsilon_prime_hex[::-1]
        
        epsilon_prime = MatrixOperations.hex_to_binary_list(epsilon_prime_hex)
        
        try:
            # Find the inverse of the matrix
            # a_inverse = self.binary_matrix.find_inverse()
            a_inverse = A_INV
            
            is_identity, _ = BinaryMatrix.verify_inverse(A, A_INV)
            
            if not is_identity:
                raise ValueError("Error in A_INVERSE calculation")
            # else :
                # print(f"Identity Matrix Success \n {identity_matrix}")
            # Multiply the inverse matrix with epsilon prime
            res_1 = BinaryMatrix.custom_multiply(a_inverse, np.array(epsilon_prime).reshape(8, 1))
            
            # Convert the result to integer and hexadecimal
            res_1_int, _ = BinaryMatrix.bin_arr_to_hex(res_1)
            # print("(a_1*ε) in hex : ", _)
            # print("(a_1*ε) in int : ", res_1_int)
            
            # Perform the field multiplication
            res_2 = gf_mult(c, res_1_int)
            # print(f"{c}.(a_1*{epsilon}) gmul : {hex(res_2)}")
            
            set_s = set()
            
            for e in self.E1:
                res_3 = gf_mult(int(e, 16), res_2)
                res_4 = gf_inverse(res_3)
                set_s.add(hex(res_4))
                # print(f"e : {e} | (c.(a_1*ε).e)_1 : {res_4}")
                
            return set_s

        except ValueError as e:
            print(f"Error: {e}")


    @DeprecationWarning
    def trial_compute_set(self, hex_num):
        set_s = set()
            
        for e in self.E1:
            res_3 = gf_mult(int(e, 16), int(hex_num, 16))
            res_4 = gf_inverse(res_3)
            set_s.add(hex(res_4))
            # print(f"e : {e} | (c.(a_1*ε).e)_1 : {res_4}")
                
        return set_s
    
    def find_solve(self, search_value):
        pairs = get_e1()[1]
        result = [hex(first) for first, second in pairs if second == search_value]
        return result
        
# Example usage
# epsilon_in_hex = 'E7'
# c = 2

# operations = MatrixOperations()
# operations.computeSet(epsilon_in_hex, c)
