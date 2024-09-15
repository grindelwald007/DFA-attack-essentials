import numpy as np

class BinaryMatrix:
    def __init__(self, matrix):
        if matrix.shape != (8, 8):
            raise ValueError("Matrix must be 8x8.")
        self.matrix = matrix
        self.inverse = None

    def xor(self, a, b):
        return a ^ b

    def matrix_multiply_gf2(self, A, B):
        result = np.zeros_like(A)
        for i in range(A.shape[0]):
            for j in range(B.shape[1]):
                for k in range(A.shape[1]):
                    result[i, j] ^= A[i, k] & B[k, j]
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
                    augmented[j] = self.xor(augmented[j], augmented[i])

        # Back-substitution
        for i in range(n-1, 0, -1):
            for j in range(i):
                if augmented[j, i] == 1:
                    augmented[j] = self.xor(augmented[j], augmented[i])

        self.inverse = augmented[:, n:]
        return self.inverse

    def verify_inverse(self):
        if self.inverse is None:
            raise ValueError("Inverse not computed yet. Call find_inverse() first.")

        product = self.matrix_multiply_gf2(self.matrix, self.inverse)
        if np.array_equal(product, np.eye(8, dtype=int)):
            return True, product
        else:
            return False, product

