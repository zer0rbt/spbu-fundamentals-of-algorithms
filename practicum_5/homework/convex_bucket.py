import queue
from time import perf_counter
from typing import Any

import numpy as np
from numpy.typing import NDArray

from src.plotting import plot_points


# Next two funcs stolen from slow_convex_hull
def signed_area(p: NDArray, q: NDArray, r: NDArray) -> int:
    signed_area = np.linalg.det(
        np.array(
            [
                np.concatenate((p, [1])),
                np.concatenate((q, [1])),
                np.concatenate((r, [1])),
            ]
        )
    )
    # if np.abs(signed_area) < 0.1:
    #    print(int(np.rint(signed_area)))
    return int(
        np.rint(signed_area)
    )  # check what happens if we use "return signed_area" instead!


def isclose(p: NDArray, q: NDArray) -> bool:
    return np.isclose(p, q).all()


def convex_bucket(points: NDArray) -> NDArray:
    """Complexity: O(n log n)"""

    # Sort the points first by y-coordinate and then by x-coordinate
    sorted_points = points[np.lexsort((points[:, 0], points[:, 1]))]

    if len(sorted_points) <= 1:
        return sorted_points

    # Compute the lower hull using Andrew's monotone chain algorithm
    lower_hull = queue.LifoQueue()
    for point in sorted_points:
        while lower_hull.qsize() >= 2 and signed_area(lower_hull.queue[-2], lower_hull.queue[-1], point) <= 0:
            lower_hull.get()
        lower_hull.put(point)

    # Convert the LifoQueue to a numpy array and remove any vertical lines of points at the edges
    clockwise_sorted_ch = np.array(list(lower_hull.queue))
    if np.isclose(clockwise_sorted_ch[0][0], clockwise_sorted_ch[1][0]):
        clockwise_sorted_ch = clockwise_sorted_ch[1:]
    if np.isclose(clockwise_sorted_ch[-2][0], clockwise_sorted_ch[-1][0]):
        clockwise_sorted_ch = clockwise_sorted_ch[:-1]

    return clockwise_sorted_ch


if __name__ == "__main__":
    for i in range(10, 11):
        txtpath = f"practicum_5/homework/points_{i}.txt"
        points = np.loadtxt(txtpath)
        print(f"Processing {txtpath}")
        print("-" * 32)
        t_start = perf_counter()
        ch = convex_bucket(points)
        t_end = perf_counter()
        print(f"Elapsed time: {t_end - t_start} sec")
        plot_points(points, convex_hull=ch, markersize=20)
        print()
