'''
    c = Mix Column Co-efficient (known)
    epsilon_prime = Differential Fault Values (known)
    epsilon = possible faults (need to calculate)
    
    * = Galois field (GF(2) in this case) Matrix Multiplication
    
    c.(a_1 * epsilon_prime) = epsilon
    
    we have 4 Eqn,
        2.(a_1 * epsilon_prime) = 0x12
        1.(a_1 * epsilon_prime) = 0x7c
        1.(a_1 * epsilon_prime) = 0x65
        3.(a_1 * epsilon_prime) = 0xb0

    we have 4 correct values for epsilon, which, in order of the Eqn, are
        ['0x12', '0x7c', '0x65', '0xb0']
        
    Now, 
        c.(a_1 * epsilon_prime) = epsilon
    =>  (a_1 * epsilon_prime) = epsilon.c_inv
    =>  (a * a_1 * epsilon_prime) = a * (epsilon.c_inv)
    =>  epsilon_prime = a * (epsilon.c_inv)
'''

from solution_set import MatrixOperations, A as A
from e1_image_set import gf_mult as gf_mult, inverse_gf2m_field as gf_inv
from binary_matrix import BinaryMatrix
import numpy as np

epsilons = ['0x12', '0x7c', '0x65', '0xb0']
epsilon_primes = ['0xe7', '0x51', '0x47', '0x99']
c = [2, 1, 1, 3]

for i in range(0,4):
    hex_value = int(epsilons[i], 16)
    inverse_value = gf_inv(c[i])
    multiplied_value = gf_mult(hex_value, inverse_value)
    binary_list = np.array(MatrixOperations.hex_to_binary_list(hex(multiplied_value))).reshape(8, 1)
    epsilon_prime = BinaryMatrix.custom_multiply(A, binary_list)

    print(f"real epsilon prime : {epsilon_primes[i]} --->calculated epsilon_prime : {BinaryMatrix.bin_arr_to_hex(epsilon_prime)}")
