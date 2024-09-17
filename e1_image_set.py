FIELD_SIZE = 256

# Function to perform multiplication in GF(2^8) using the irreducible polynomial
def gf_mult(a, b, mod=0x11b):
    p = 0
    while a and b:
        if b & 1:
            p ^= a
        if a & 0x80:
            a = (a << 1) ^ mod
        else:
            a <<= 1
        b >>= 1
    return p & 0xFF  # Ensure the result is within 8 bits

# Function to calculate f(x) = x^2 + x in GF(2^8)
def gf_calculate(x):
    # Square x in GF(2^8)
    x_squared = gf_mult(x, x)
    # f(x) = x^2 + x (which is just x_squared ^ x in GF(2^8))
    return x_squared ^ x

def generate_mapping():
    i = 0
    list_of_pairs = []
    while i <= 255 :
        x = i
        i = i + 1
        try:
            # Ensure the input is a valid 8-bit number
            if x < 0 or x > 0xFF:
                print("Please enter a valid 8-bit hexadecimal value (00 to FF).")
                continue
        
            # Calculate f(x)
            fx = gf_calculate(x)
            new_pair = (x, fx)
            list_of_pairs.append(new_pair)
            # Print x and f(x) in hexadecimal format
            # print(f"x = 0x{x:02X}")
            # print(f"f(x) = 0x{fx:02X}")
        except ValueError:
            print("Invalid input. Please enter a valid hexadecimal number.")
    
    E1 = []
    for pair in list_of_pairs:
        hex_pair = (hex(pair[0]), hex(pair[1]))
        # print(hex_pair)
        E1.append(hex_pair[1])
    return E1, list_of_pairs
    
def inverse_gf2m_field(a):
    d = FIELD_SIZE - 2
    return exp(a, d)

def exp(a, k):
    if a == 0:
       return 0
    if a == 1:
        return 1

    result = 1
    if k < 0:
        a = inverse_gf2m_field(a)
        k = -k

    while k != 0:
        if k & 1 == 1:
            result = gmul(result, a)
        a = gmul(a, a)
        k >>= 1

    return result

def gmul(a, b):
    # Galois Field multiplication
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        if hi_bit_set:
            a ^= 0x1b  # The reduction polynomial x^8 + x^4 + x^3 + x + 1
        b >>= 1
    return p % FIELD_SIZE
    

# generate_mapping()

# print(f"gmul(123, 213) {gmul(123, 213)}" )

# print(f"gf_mult(123, 213) {gf_mult(123, 213)}" )
