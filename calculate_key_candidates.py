from solution_set import MatrixOperations, A as A, A_INV as A_INV
from e1_image_set import gf_mult as gf_mult, inverse_gf2m_field as gf_inv
from binary_matrix import BinaryMatrix
import numpy as np

Sbox = (    
            0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
            0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
            0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
            0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
            0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
            0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
            0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
            0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
            0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
            0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
            0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
            0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
            0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
            0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
            0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
            0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
        )

    # mix column coefficient
MCC = [2, 1, 1, 3]
def get_sbox_val(val):
    return Sbox[val]

def is_theta_element_of_e1(theta):
    mo = MatrixOperations()
    e1_star = mo.get_e1_star_list()
    if theta in e1_star:
        return True
    else:
        return False

def calculate_key_candidates(ep, f_nr_ai, i):
    set_1 = {}
    set_2 = {}
    set_3 = {}
    set_4 = {}

    mo = MatrixOperations()
    # Sc,ε0 = {(c.(a−1 ∗ ε0).e)−1, e ∈ E1}
    
    # "e7" "51" "47" "99"
    set_1 = mo.compute_set(MCC[0], ep[0])
    set_2 = mo.compute_set(MCC[1], ep[1]) 
    set_3 = mo.compute_set(MCC[2], ep[2])
    set_4 = mo.compute_set(MCC[3], ep[3])

    intersection = set_1.intersection(set_2, set_3, set_4)
    s_intersec = sorted(intersection)

    # logging.debug(f"s_intersec\n{s_intersec}\n") 

    result = []
    c = 2
    epsilon_prime = ep[0][::-1]
    if i == 0 or i == 1 or i == 2 or i == 3:
        c = MCC[0]
        epsilon_prime = ep[0][::-1]
    elif i == 7 or i == 4 or i == 5 or i == 6:
        c = MCC[1]
        epsilon_prime = ep[1][::-1]
    elif i == 10 or i == 11 or i == 8 or i == 9:
        c = MCC[2]
        epsilon_prime = ep[2][::-1]
    elif i == 13 or i == 14 or i == 15 or i == 12:
        c = MCC[3]
        epsilon_prime = ep[3][::-1]

    epsilon_prime = MatrixOperations.hex_to_binary_list(epsilon_prime)
    res_1 = BinaryMatrix.custom_multiply(A_INV, np.array(epsilon_prime).reshape(8, 1))
     
    res_1_int, _ = BinaryMatrix.bin_arr_to_hex(res_1)
    
    res_2 = gf_mult(c, res_1_int)
    # logging.debug(f"{c}.(a_1*{ep_2}) gmul : {hex(res_2)}")

    for epsilon in s_intersec:
        # θ = ((a−1 ∗ε0).c.ε)−1 ∈ E∗
        
        a_inv_mul_epsilon_prime_dot_c = res_2
        epsilon_int = int(epsilon, 16)
        res1 = gf_mult(a_inv_mul_epsilon_prime_dot_c, epsilon_int)
        theta = gf_inv(res1)
    
        if is_theta_element_of_e1(theta):
            raise ValueError(f"Theta value {theta} is not an element of E1* and is not allowed.")

        # find solve for t : t^2 + t = θ; solves, alpha and beta
    
        alphas = mo.find_solve(theta)
        if len(alphas) != 0:
            faulty_state_nr_a_i = f_nr_ai
            gmul_c_epsilon = gf_mult(c, epsilon_int)
            s_c_epsilon_alpha = get_sbox_val(gf_mult(gmul_c_epsilon, int(alphas[0], 16)))
            s_c_epsilon_beta = get_sbox_val(gf_mult(gmul_c_epsilon, int(alphas[1], 16)))
        
            # s(c.ε.α) + F_Nr,A[i] or,  s(c.ε.β) + F_Nr,A[i]
            res1 = s_c_epsilon_alpha ^ faulty_state_nr_a_i
            res2 = s_c_epsilon_beta ^ faulty_state_nr_a_i
        
            result.append(hex(res1) if res1>=0x10 else f'0x{res1:02x}')
            result.append(hex(res2) if res2>=0x10 else f'0x{res2:02x}')
        
            if theta == 1:
                b = 0x63
                res3 = b ^ faulty_state_nr_a_i
                result.append(hex(res3) if res3>=0x10 else f'0x{res3:02x}')
                s_c_epsilon = get_sbox_val(gmul_c_epsilon)
                res4 = s_c_epsilon ^ faulty_state_nr_a_i
                result.append(hex(res4) if res4>=0x10 else f'0x{res4:02x}')

    # logging.debug(f"final result : {sorted(result)}")
    return sorted(result)