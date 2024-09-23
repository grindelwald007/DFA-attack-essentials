import calculate_key_candidates as kc
import faulty_aes_simulator as df


def calc_k_0_0_10_key(fault):
    dif_fault_list, f_Nr_A_0 = df.get_differential_faults(fault, 0, 0)
    ep0 = 0
    ep1 = 0
    ep2 = 0
    ep3 = 0
    for i in range(0, 4):
        (ep, (row, col)) = dif_fault_list[i]
        if row == 0 and col == 0:
            ep0 = ep.replace("0x", "").zfill(2)
        elif row == 1 and col == 3:
            ep1 = ep.replace("0x", "").zfill(2)
        elif row == 2 and col == 2:
            ep2 = ep.replace("0x", "").zfill(2)
        elif row == 3 and col == 1:
            ep3 = ep.replace("0x", "").zfill(2)

    return kc.calculate_key_candidates(ep0, ep1, ep2, ep3, f_Nr_A_0)

list_1 = calc_k_0_0_10_key(0x1e)
# print(f"list_1 {list_1}\n")

list_2 = calc_k_0_0_10_key(0xe1)
# print(f"list_2 {list_2}\n")

list_3 = calc_k_0_0_10_key(0xb3)
# print(f"list_3 {list_3}\n")

list_4 = calc_k_0_0_10_key(0x16)
# print(f"list_4 {list_4}\n")

list_5 = calc_k_0_0_10_key(0x9e)
# print(f"list_5 {list_5}\n")

set_1 = set(list_1)
set_2 = set(list_2)
set_3 = set(list_3)
set_4 = set(list_4)
set_5 = set(list_5)

print(sorted(set_1))
print(set_1.intersection(set_2))
print(set_1.intersection(set_2, set_3))
print(set_1.intersection(set_2, set_3, set_4))
print(set_1.intersection(set_2, set_3, set_4, set_5))