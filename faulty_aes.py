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
    ((0xe1, 0, 0), (1, 1)),
    ((0xb3, 0, 0), (1, 1)),
    ((0x16, 0, 0), (1, 1)),
    ((0x9e, 0, 0), (1, 1)),
    
    # ((0x1e, 0, 1), (1, 1)),
    # ((0xe1, 0, 1), (1, 1)),
    # ((0xb3, 0, 1), (1, 1)),
    # ((0x16, 0, 1), (1, 1)),
    # ((0x9e, 0, 1), (1, 1)),
    
    # ((0x1e, 0, 2), (1, 1)),
    # ((0xe1, 0, 2), (1, 1)),
    # ((0xb3, 0, 2), (1, 1)),
    # ((0x16, 0, 2), (1, 1)),
    # ((0x9e, 0, 2), (1, 1)),
    
    # ((0x1e, 0, 3), (1, 1)),
    # ((0xe1, 0, 3), (1, 1)),
    # ((0xb3, 0, 3), (1, 1)),
    # ((0x16, 0, 3), (1, 1)),
    # ((0x9e, 0, 3), (1, 1))
]

def search_by_fault_tuple(target_fault):
    for fault in FAULT_TUPLE:
        if fault[0] == target_fault:
            return fault[1]
    return None


def get_differential_faults(fault, fault_row, fault_col):
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