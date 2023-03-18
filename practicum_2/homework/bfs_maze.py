import queue
from time import perf_counter


class Maze:
    def __init__(self, list_view: list[list[str]]) -> None:
        self.list_view = list_view
        self.start_j = None
        for j, sym in enumerate(self.list_view[0]):
            if sym == "O":
                self.start_j = j

    @classmethod
    def from_file(cls, filename):
        list_view = []
        with open(filename, "r") as f:
            for l in f.readlines():
                list_view.append(list(l.strip()))
        obj = cls(list_view)
        return obj

    def print(self, path="") -> None:
        # Find the path coordinates
        i = 0  # in the (i, j) pair, i is usually reserved for rows and j is reserved for columns
        j = self.start_j
        path_coords = set()
        for move in path:
            i, j = _shift_coordinate(i, j, move)
            path_coords.add((i, j))
        # Print maze + path
        for i, row in enumerate(self.list_view):
            for j, sym in enumerate(row):
                if (i, j) in path_coords:
                    print("+ ", end="")  # NOTE: end is used to avoid linebreaking
                else:
                    print(f"{sym} ", end="")
            print()  # linebreak


def move_rate(i: int, j: int) -> str:
    try:
        if maze.list_view[i][j] == " ":
            return "ok"
        elif maze.list_view[i][j] == "X":
            return "win"
    except IndexError:  # We need that in case of trying to move out from maze
        pass
    return "bad"


# Note: variable-naming here is bad, but in other tasks it is better, at least I hope so.
def solve(maze: Maze) -> None:
    path = ""  # solution as a string made of "L", "R", "U", "D"

    was_set = set()
    paths_list = queue.Queue()

    # Elements in queue (using numpy syntax) have this dtype:
    # [("cell_coordinates", int, (2, )), ("way_to_cell", str, _rand_int_)]
    paths_list.put(((1, maze.start_j), "D"))
    while not paths_list.empty():
        current_cell = paths_list.get()
        if current_cell[0] in was_set:
            continue

        was_set.add(current_cell[0])
        possible_ways = ["U", "L", "D", "R"]

        rated_ways_list = list(map(lambda w: move_rate(*_shift_coordinate(*current_cell[0], w)), possible_ways))

        for way in range(4):
            # Guard statement to secure ways rated as "bad"
            if rated_ways_list[way] == "bad":
                continue

            # Win-check and adding "good" possible_ways into queue.
            if rated_ways_list[way] == "win":
                path = current_cell[1] + possible_ways[way]

                print(f"Found: {path}")
                maze.print(path)
                return None  # This "return" escaping all "for" and "while" cycles in one line
            else:
                paths_list.put((
                    _shift_coordinate(*current_cell[0], possible_ways[way]), current_cell[1] + possible_ways[way]))


def _shift_coordinate(i: int, j: int, move: str) -> tuple[int, int]:
    if move == "L":
        j -= 1
    elif move == "R":
        j += 1
    elif move == "U":
        i -= 1
    elif move == "D":
        i += 1
    return i, j


if __name__ == "__main__":
    maze = Maze.from_file("maze_2.txt")  # I had "FileNotFoundError" on old path.
    t_start = perf_counter()
    solve(maze)
    t_end = perf_counter()
    print(f"Elapsed time: {t_end - t_start} sec")
