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


def points_below_line(points: NDArray, p: NDArray, q: NDArray) -> NDArray:
    return np.array(list(filter(lambda x: signed_area(x, p, q) <= 0, points)))


def convex_bucket(points: NDArray) -> NDArray:
    """Complexity: O(n log n)"""

    # Compute the lower hull using Andrew's monotone chain algorithm
    if len(points) <= 1:
        return points

    # Sort the points first by y-coordinate and then by x-coordinate
    sorted_points = points[np.lexsort((points[:, 1], points[:, 0]))]

    # Excluding points that have not [min Y-cord from points with max X-cord]
    for i in range(len(sorted_points)- 1, 0, -1):
        if sorted_points[i][0] != sorted_points[i - 1][0]:
            break
    sorted_points = sorted_points[:i + 1]

    # Excluding points below [min X: min Y from (points with min X)] & [max X: min Y from (points with max X)]
    # This optimisation saves up to 60% of time on given examples
    sorted_points = points_below_line(sorted_points, sorted_points[0], sorted_points[-1])

    lower_hull = queue.LifoQueue()
    for point in sorted_points:
        while signed_area(lower_hull.queue[-2], lower_hull.queue[-1], point) <= 0 and lower_hull.qsize() >= 2:
            lower_hull.get()
        lower_hull.put(point)

    # Convert the LifoQueue to a numpy array and remove any vertical lines of points at the edges
    clockwise_sorted_ch = np.array(list(lower_hull.queue[::-1]))
    if np.isclose(clockwise_sorted_ch[0][0], clockwise_sorted_ch[1][0]):
        clockwise_sorted_ch = clockwise_sorted_ch[1:]

    return clockwise_sorted_ch


if __name__ == "__main__":
    for i in range(1, 11):
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