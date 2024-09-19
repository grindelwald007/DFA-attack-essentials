import numpy as np

class BinaryMatrix:
    def __init__(self, matrix):
        if matrix.shape != (8, 8):
            raise ValueError("Matrix must be 8x8.")
        self.matrix = matrix
        self.inverse = None

    @staticmethod
    def xor(a, b):
        return a ^ b

    @staticmethod
    def matrix_multiply_gf2(a, b):
        result = np.zeros_like(a)
        for i in range(a.shape[0]):
            for j in range(b.shape[1]):
                for k in range(a.shape[1]):
                    result[i, j] ^= a[i, k] & b[k, j]
        return result

    def find_inverse(self):
        matrix = self.matrix.copy()
        n = 8
        augmented = np.hstack((matrix, np.eye(n, dtype=int)))

        # Gaussian elimination
        for i in range(n):
            if augmented[i, i] == 0:
                for j in range(i+1, n):
                    if augmented[j, i] == 1:
                        augmented[i], augmented[j] = augmented[j].copy(), augmented[i].copy()
                        break
                else:
                    raise ValueError("Matrix is not invertible")
            for j in range(i+1, n):
                if augmented[j, i] == 1:
                    augmented[j] = BinaryMatrix.xor(augmented[j], augmented[i])

        # Back-substitution
        for i in range(n-1, 0, -1):
            for j in range(i):
                if augmented[j, i] == 1:
                    augmented[j] = BinaryMatrix.xor(augmented[j], augmented[i])

        self.inverse = augmented[:, n:]
        return self.inverse

    def verify_inverse(self):
        if self.inverse is None:
            raise ValueError("Inverse not computed yet. Call find_inverse() first.")

        product = BinaryMatrix.matrix_multiply_gf2(self.matrix, self.inverse)
        if np.array_equal(product, np.eye(8, dtype=int)):
            return True, product
        else:
            return False, product
        
    @staticmethod
    def verify_inverse(a_matrix, a_inv_matrix):
        product = BinaryMatrix.matrix_multiply_gf2(a_matrix, a_inv_matrix)
        if np.array_equal(product, np.eye(8, dtype=int)):
            return True, product
        else:
            return False, product

    @staticmethod
    def custom_multiply(matrix, vector):
        if matrix.shape != (8, 8) or vector.shape != (8, 1):
            raise ValueError("Matrix must be 8x8 and vector must be 8x1.")
    
        result = np.zeros(8, dtype=int)
    
        for i in range(8):
            temp_result = 0
            for j in range(8):
                temp_result = temp_result ^ (matrix[i, j] & vector[j])
            result[i] = temp_result
    
        return result
    
    @staticmethod
    def bin_arr_to_hex(binary_list):
        binary_string = ''.join(map(str, binary_list))
        decimal_value = int(binary_string, 2)
        hex_value = hex(decimal_value)
        return (decimal_value, hex_value)

