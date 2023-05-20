import numpy as np
from numpy.typing import NDArray

mply = np.matmul
inv = np.linalg.inv


def lu(A: NDArray, permute: bool) -> tuple[NDArray, NDArray, NDArray]:
    n = A.shape[0]
    L = np.eye(n)
    U = np.copy(A)
    P = np.eye(n)
    try:
        for k in range(n - 1):
        # Partial Pivoting

            if permute:
                max_index = np.argmax(np.abs(U[k:, k])) + k
                if max_index != k:
                    U[[k, max_index], :] = U[[max_index, k], :]  # Swap rows in U
                    P[[k, max_index], :] = P[[max_index, k], :]  # Swap rows in P
                    if k >= 1:
                        L[[k, max_index], :k] = L[[max_index, k], :k]  # Swap rows in L before k

        for j in range(k + 1, n):
            L[j, k] = U[j, k] / U[k, k]
            U[j, k:] -= L[j, k] * U[k, k:]

    return L, U, P


def solve(L: NDArray, U: NDArray, P: NDArray, b: NDArray) -> NDArray:
    print(P)
    print(L)
    print(U)
    print(mply(L, U))
    Y = mply(inv(L), mply(P, b))
    X = mply(inv(U), np.transpose(Y))
    return X


def get_A_b(a_11: float, b_1: float) -> tuple[NDArray, NDArray]:
    A = np.array([[a_11, 1.0, -3.0], [6.0, 2.0, 5.0], [1.0, 4.0, -3.0]])
    b = np.array([b_1, 12.0, -39.0])
    return A, b


if __name__ == "__main__":
    # Let's implement the LU decomposition with and without pivoting
    # and check its stability depending on the matrix elements
    p = 16  # modify from 7 to 16 to check instability
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
