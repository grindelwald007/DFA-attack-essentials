import os, logging
import numpy as np
import calculate_key_candidates as kc, faulty_aes_simulator as df1
import faulty_aes as df2

log_folder = 'logs'

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file = os.path.join(log_folder, 'orchestrator.log')

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def get_faulty_enc_state_value(faulty_enc_state, key_pos):
    if key_pos == 0:
        return faulty_enc_state[0, 0]
    elif key_pos == 7:
        return faulty_enc_state[1, 3]
    elif key_pos == 10:
        return faulty_enc_state[2, 2]
    elif key_pos == 13:
        return faulty_enc_state[3, 1]
    elif key_pos == 1:
        return faulty_enc_state[0, 1]
    elif key_pos == 4:
        return faulty_enc_state[1, 0]
    elif key_pos == 11:
        return faulty_enc_state[2, 3]
    elif key_pos == 14:
        return faulty_enc_state[3, 2]
    elif key_pos == 2:
        return faulty_enc_state[0, 2]
    elif key_pos == 5:
        return faulty_enc_state[1, 1]
    elif key_pos == 8:
        return faulty_enc_state[2, 0]
    elif key_pos == 15:
        return faulty_enc_state[3, 3]
    elif key_pos == 3:
        return faulty_enc_state[0, 3]
    elif key_pos == 6:
        return faulty_enc_state[1, 2]
    elif key_pos == 9:
        return faulty_enc_state[2, 1]
    elif key_pos == 12:
        return faulty_enc_state[3, 0]
    else:
        raise ValueError(f"Invalid key position: {key_pos}")


def calc_k_10_key_candidates(fault, key_pos, fault_col, fault_row = 0):
    dif_fault_list, faulty_enc_state = df1.get_differential_faults(fault, fault_row, fault_col)
    
    logging.debug(f"{fault}, {fault_row}, {fault_col} ")
    
    # dif_fault_list, faulty_enc_state = df2.get_differential_faults(fault, 
    # fault_row, fault_col)
    
    ep = ['00', '00', '00', '00']  # Initialize ep array with default values

    f_nr_a_i = get_faulty_enc_state_value(faulty_enc_state, key_pos)
    
    for i in range(0, 4):
        (ep_value, (row, col)) = dif_fault_list[i]
        ep_value = ep_value.replace("0x", "").zfill(2)
        if (row == 0 and col == 0) or (row == 0 and col == 1) or (row == 0 and col == 2) or (row == 0 and col == 3):
            ep[0] = ep_value
        elif (row == 1 and col == 3) or (row == 1 and col == 0) or (row == 1 and col == 1) or (row == 1 and col == 2):
            ep[1] = ep_value
        elif (row == 2 and col == 2) or (row == 2 and col == 3) or (row == 2 and col == 0) or (row == 2 and col == 1):
            ep[2] = ep_value
        elif (row == 3 and col == 1) or (row == 3 and col == 2) or (row == 3 and col == 3) or (row == 3 and col == 0):
            ep[3] = ep_value

    return kc.calculate_key_candidates(ep, f_nr_a_i, key_pos)


def get_k_10_single_byte(fault_lists, key_pos):
    fault_inject_row = 0
    fault_inject_col = 0
    
    if key_pos == 0 or key_pos == 7 or key_pos == 10 or key_pos == 13:
        fault_inject_row = 0
        fault_inject_col = 0
    elif key_pos == 1 or key_pos == 4 or key_pos == 11 or key_pos == 14:
        fault_inject_row = 0
        fault_inject_col = 1
    elif key_pos == 2 or key_pos == 5 or key_pos == 8 or key_pos == 15:
        fault_inject_row = 0
        fault_inject_col = 2
    elif key_pos == 3 or key_pos == 6 or key_pos == 9 or key_pos == 12:
        fault_inject_row = 0
        fault_inject_col = 3
        
    list_1 = calc_k_10_key_candidates(fault_lists[0], key_pos, fault_inject_col, fault_inject_row)
    list_2 = calc_k_10_key_candidates(fault_lists[1], key_pos, fault_inject_col, fault_inject_row)
    list_3 = calc_k_10_key_candidates(fault_lists[2], key_pos, fault_inject_col, fault_inject_row)
    list_4 = calc_k_10_key_candidates(fault_lists[3], key_pos, fault_inject_col, fault_inject_row)
    list_5 = calc_k_10_key_candidates(fault_lists[4], key_pos, fault_inject_col, fault_inject_row)

    set_1 = set(list_1)
    set_2 = set(list_2)
    set_3 = set(list_3)
    set_4 = set(list_4)
    set_5 = set(list_5)

    # logging.debug(sorted(set_1))
    # logging.debug(set_1.intersection(set_2))
    # logging.debug(set_1.intersection(set_2, set_3))
    # logging.debug(set_1.intersection(set_2, set_3, set_4))
    # logging.debug(f"Key[10][{key_pos}]={set_1.intersection(set_2, set_3, set_4, set_5)}")
    
    res = set_1.intersection(set_2, set_3, set_4, set_5)
    
    if len(res) == 1:
        return list(res)[0]
    else :
        raise ValueError(f"Error getting key of position {key_pos}.")
    
    
key_10 = np.empty((4, 4), dtype=object)

FAULT_INJECTION_LIST = [0x1e, 0xe1, 0xb3, 0x16, 0x9e]

key_10[0, 0] = get_k_10_single_byte(FAULT_INJECTION_LIST, 0)
key_10[1, 3] = get_k_10_single_byte(FAULT_INJECTION_LIST, 7)
key_10[2, 2] = get_k_10_single_byte(FAULT_INJECTION_LIST, 10)
key_10[3, 1] = get_k_10_single_byte(FAULT_INJECTION_LIST, 13)

key_10[0, 1] = get_k_10_single_byte(FAULT_INJECTION_LIST, 1)
key_10[1, 0] = get_k_10_single_byte(FAULT_INJECTION_LIST, 4)
key_10[2, 3] = get_k_10_single_byte(FAULT_INJECTION_LIST, 11)
key_10[3, 2] = get_k_10_single_byte(FAULT_INJECTION_LIST, 14)

key_10[0, 2] = get_k_10_single_byte(FAULT_INJECTION_LIST, 2)
key_10[1, 1] = get_k_10_single_byte(FAULT_INJECTION_LIST, 5)
key_10[2, 0] = get_k_10_single_byte(FAULT_INJECTION_LIST, 8)
key_10[3, 3] = get_k_10_single_byte(FAULT_INJECTION_LIST, 15)

key_10[0, 3] = get_k_10_single_byte(FAULT_INJECTION_LIST, 3)
key_10[1, 2] = get_k_10_single_byte(FAULT_INJECTION_LIST, 6)
key_10[2, 1] = get_k_10_single_byte(FAULT_INJECTION_LIST, 9)
key_10[3, 0] = get_k_10_single_byte(FAULT_INJECTION_LIST, 12)


logging.debug(f"key_10 \n{key_10}")

with open('keys/Key_10.txt', 'w') as file:
    file.write(str(key_10))