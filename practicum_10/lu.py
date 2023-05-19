import numpy as np
from numpy.typing import NDArray

mply = np.matmul
inv = np.linalg.inv


def lu(A: NDArray, permute: bool) -> tuple[NDArray, NDArray, NDArray]:
    n = int(A.size ** 0.5)
    M = np.eye(n)
    P = np.eye(n)
    for i in range(n - 1):
        if permute:
            pass
        for j in range(i + 1, n):
            M[j][i] = A[j][i] / A[i][i]
            A[j] -= A[i] * M[j][i]
        print(M)
    L = M
    U = mply(inv(L), A)
    return L, U, P


def solve(L: NDArray, U: NDArray, P: NDArray, b: NDArray) -> NDArray:
    Y = mply(inv(L), mply(P, b))
    X = mply(inv(U), Y)
    return X


def get_A_b(a_11: float, b_1: float) -> tuple[NDArray, NDArray]:
    A = np.array([[a_11, 1.0, -3.0], [6.0, 2.0, 5.0], [1.0, 4.0, -3.0]])
    b = np.array([b_1, 12.0, -39.0])
    return A, b


if __name__ == "__main__":
    # Let's implement the LU decomposition with and without pivoting
    # and check its stability depending on the matrix elements
    p = 14  # modify from 7 to 16 to check instability
    a_11 = 3 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    b_1 = -16 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    A, b = get_A_b(a_11, b_1)
    # With pivoting
    L, U, P = lu(A, permute=True)
    x = solve(L, U, P, b)
    assert np.all(np.isclose(x, [1, -7, 4])), f"The anwser {x} is not accurate enough"
    # Without pivoting
    L, U, P = lu(A, permute=False)
    x_ = solve(L, U, P, b)
    assert np.all(np.isclose(x_, [1, -7, 4])), f"The anwser {x_} is not accurate enough"
