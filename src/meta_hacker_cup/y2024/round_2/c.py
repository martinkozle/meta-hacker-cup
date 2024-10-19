# INCOMPLETE SOLUTION

from collections import defaultdict
from collections.abc import MutableMapping


def main() -> None:
    T = int(input())
    for t in range(T):
        R, C, K = map(int, input().split())
        grid: list[list[int]] = []
        for r in range(R):
            grid.append(list(map(int, input().split())))

        # print("precomputing...")

        running_sums_row: MutableMapping[tuple[int, int, int], int] = defaultdict(
            lambda: 0
        )
        running_sums_col: MutableMapping[tuple[int, int, int], int] = defaultdict(
            lambda: 0
        )
        unique_elements: set[int] = set(element for row in grid for element in row)

        # print("rows...")

        for r, row in enumerate(grid):
            for c, bunny in enumerate(row):
                running_sums_row[r, c, bunny] = 1
                for prev in range(c - 1, -1, -1):
                    if running_sums_row[r, prev, bunny] != 0:
                        running_sums_row[r, c, bunny] = (
                            running_sums_row[r, prev, bunny] + 1
                        )
            for c in range(len(row), len(row) + max(R, C) * 2):
                for unique_element in unique_elements:
                    running_sums_row[r, c, unique_element] = running_sums_row[
                        r, c - 1, unique_element
                    ]

        # print("columns...")

        for c in range(C):
            column = [row[c] for row in grid]
            for r, bunny in enumerate(column):
                running_sums_col[r, c, bunny] = 1
                for prev in range(c - 1, -1, -1):
                    if running_sums_col[r, prev, bunny] != 0:
                        running_sums_col[r, c, bunny] = (
                            running_sums_col[prev, c, bunny] + 1
                        )
                for unique_element in unique_elements:
                    running_sums_col[r, c, unique_element] = running_sums_col[
                        r - 1, c, unique_element
                    ] + (1 if bunny == unique_element else 0)
            for r in range(len(column), len(column) + max(R, C) * 2):
                for unique_element in unique_elements:
                    running_sums_col[r, c, unique_element] = running_sums_col[
                        r - 1, c, unique_element
                    ]

        # print("main calculation...")

        scores: dict[int, int] = {}
        for dist in range(1, max(R, C)):
            # print(f"{dist=}")
            scores[dist] = 0
            for r in range(R):
                for c in range(C):
                    bunny = grid[r][c]
                    left = (
                        dist * 2
                        + 1
                        - (
                            running_sums_col[r + dist, c - dist, bunny]
                            - running_sums_col[r - dist, c - dist, bunny]
                        )
                    )
                    right = (
                        dist * 2
                        + 1
                        - (
                            running_sums_col[r + dist, c + dist, bunny]
                            - running_sums_col[r - dist, c + dist, bunny]
                        )
                    )
                    top = (
                        dist * 2
                        + 1
                        - (
                            running_sums_row[r - dist, c + dist, bunny]
                            - running_sums_row[r - dist, c - dist, bunny]
                        )
                    )
                    bottom = (
                        dist * 2
                        + 1
                        - (
                            running_sums_row[r + dist, c + dist, bunny]
                            - running_sums_row[r + dist, c - dist, bunny]
                        )
                    )
                    # print(f"{bunny=},{r=},{c=},{left=},{right=},{top=},{bottom=}")
                    scores[dist] += left + right + top + bottom

        # print(scores)

        for k, v in sorted(scores.items()):
            if K - v > 0:
                K -= v
            else:
                print(f"Case #{t+1}: {k}")
                break
        else:
            raise RuntimeError("Unexpected state")


if __name__ == "__main__":
    main()
