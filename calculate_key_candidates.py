from solution_set import MatrixOperations, A as A, A_INV as A_INV
from e1_image_set import gf_mult as gf_mult, inverse_gf2m_field as gf_inv
from binary_matrix import BinaryMatrix
from constants import S_BOX as Sbox
import numpy as np


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