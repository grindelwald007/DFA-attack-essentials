import numpy as np
import os, logging

log_folder = 'logs'

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file = os.path.join(log_folder, 'faulty_aes.log')

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

CORRECT_CIPHER_TEXT = np.array([
    [0x39, 0x02, 0xdc, 0x19],
    [0x25, 0xdc, 0x11, 0x6a],
    [0x84, 0x09, 0x85, 0x0b],
    [0x1d, 0xfb, 0x97, 0x32]]
)

#[List of (fault, fault_row, fault_col), faulty_state)]
FAULT_TUPLE = [
    ((0x1e, 0, 0), [[222, 2, 220, 25], [37, 220, 17, 59], [132, 9, 194, 11], [29, 98, 151, 50]]),
    ((0xe1, 0, 0), [[243, 2, 220, 25], [37, 220, 17, 81], [132, 9, 113, 11], [29, 126, 151, 50]]),##
    ((0xb3, 0, 0), [[64, 2, 220, 25], [37, 220, 17, 110], [132, 9, 143, 11], [29, 249, 151, 50]]),##
    ((0x16, 0, 0), [[22, 2, 220, 25], [37, 220, 17, 210], [132, 9, 101, 11], [29, 191, 151, 50]]),##
    ((0x9e, 0, 0), [[155, 2, 220, 25], [37, 220, 17, 126], [132, 9, 92, 11], [29, 213, 151, 50]]),##

    ((0x1e, 0, 1), [[57, 132, 220, 25], [16, 220, 17, 106], [132, 9, 133, 251], [29, 251, 236, 50]]),
    ((0xe1, 0, 1), [[57, 4, 220, 25], [158, 220, 17, 106], [132, 9, 133, 57], [29, 251, 173, 50]]),
    ((0xb3, 0, 1), [[57, 255, 220, 25], [74, 220, 17, 106], [132, 9, 133, 49], [29, 251, 30, 50]]),
    ((0x16, 0, 1), [[57, 84, 220, 25], [19, 220, 17, 106], [132, 9, 133, 61], [29, 251, 102, 50]]),
    ((0x9e, 0, 1), [[57, 58, 220, 25], [243, 220, 17, 106], [132, 9, 133, 40], [29, 251, 239, 50]]),

    ((0x1e, 0, 2), [[57, 2, 72, 25], [37, 230, 17, 106], [46, 9, 133, 11], [29, 251, 151, 0]]),
    ((0xe1, 0, 2), [[57, 2, 225, 25], [37, 231, 17, 106], [112, 9, 133, 11], [29, 251, 151, 56]]),
    ((0xb3, 0, 2), [[57, 2, 163, 25], [37, 39, 17, 106], [25, 9, 133, 11], [29, 251, 151, 3]]),
    ((0x16, 0, 2), [[57, 2, 189, 25], [37, 71, 17, 106], [146, 9, 133, 11], [29, 251, 151, 103]]),
    ((0x9e, 0, 2), [[57, 2, 112, 25], [37, 155, 17, 106], [164, 9, 133, 11], [29, 251, 151, 254]]),

    ((0x1e, 0, 3), [[57, 2, 220, 122], [37, 220, 254, 106], [132, 111, 133, 11], [36, 251, 151, 50]]),
    ((0xe1, 0, 3), [[57, 2, 220, 147], [37, 220, 172, 106], [132, 47, 133, 11], [47, 251, 151, 50]]),
    ((0xb3, 0, 3), [[57, 2, 220, 133], [37, 220, 110, 106], [132, 132, 133, 11], [52, 251, 151, 50]]),
    ((0x16, 0, 3), [[57, 2, 220, 44], [37, 220, 60, 106], [132, 5, 133, 11], [51, 251, 151, 50]]),
    ((0x9e, 0, 3), [[57, 2, 220, 93], [37, 220, 115, 106], [132, 163, 133, 11], [215, 251, 151, 50]])    
]

file_path = 'keys/fault_data.txt'

def search_by_fault_tuple(target_fault):
    for fault in FAULT_TUPLE:
        if fault[0] == target_fault:
            return fault[1]
    return None


def get_differential_faults(fault, fault_row, fault_col):
    # populate_fault_tuple()
    target_fault_tuple = (fault, fault_row, fault_col)
    state_faulty = search_by_fault_tuple(target_fault_tuple)

    if state_faulty:
        logging.debug(f"Success finding for {target_fault_tuple}")
    else:
        logging.error(f"Error finding for injected fault {target_fault_tuple}")
        raise ValueError(f"Please provide correct Fault state for injected fault {hex(fault)} at row {fault_row} and col {fault_col}")
        
    state_faulty = np.array(state_faulty)
    # logging.debug(f"state_faulty \n{AesSimulator.matrix_to_hex(state_faulty)}\n")
    
    state_correct = CORRECT_CIPHER_TEXT
    # logging.debug(f"state_correct \n{AesSimulator.matrix_to_hex(state_correct)}\n")
    
    state_error = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    
    res = []
    
    for i in range(state_error.shape[0]):
        for j in range(state_error.shape[1]):
            state_error[i, j] = state_correct[i, j] ^ state_faulty[i][j]
            if state_error[i, j] != 0:
                res.append((hex(state_error[i, j]), (i, j)))
            
    # logging.debug(f"state_error \n{AesSimulator.matrix_to_hex(state_error)}\n")
    return res, state_faulty