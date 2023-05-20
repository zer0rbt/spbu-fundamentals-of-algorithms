import numpy as np
from numpy.typing import NDArray

mply = np.matmul
inv = np.linalg.inv


def absmax(A: NDArray, ind: int) -> int:
    return np.argmax(A, axis=0)[ind] if abs(np.max(A, axis=0))[ind] > abs(np.min(A, axis=0))[ind] else \
    np.argmin(A, axis=0)[ind]


def lu(A: NDArray, permute: bool) -> tuple[NDArray, NDArray, NDArray]:
    n = int(A.size ** 0.5)
    A_was = np.array(list(A))
    M = np.eye(n)
    P = np.eye(n)
    for i in range(n - 1):
        if permute:
            max_arg = i + absmax(A[i:], i)
            _ = list(A[i])
            A[i], A[max_arg] = A[max_arg], _
            _ = list(P[i])
            P[i], P[max_arg] = P[max_arg], _
        for j in range(i + 1, n):
            M[j][i] = A[j][i] / A[i][i]
            A[j] -= A[i] * M[j][i]
    L = M
    print(inv(L))
    U = mply(np.swapaxes(np.swapaxes(inv(L),0,1)[::-1], 0, 1), A_was)
    print(mply(inv(P), A_was))

    return L, A, P


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
