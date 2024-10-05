import sys
from functools import lru_cache


class Solver:
    def __init__(self, e: list[str], k: int) -> None:
        self.e = e
        self.k = k
        self.final_e: list[str] = []
        self.done: bool = False

    def rec(self, ind: int) -> None:
        if ind > len(self.e) - 2:
            self.k -= 1
            if self.k == 0:
                self.final_e = self.e.copy()
                self.done = True
            return

        prev_str = self.e[ind - 1]
        curr = self.e[ind]
        nxt_str = self.e[ind + 1]

        prev = int(prev_str) if prev_str.isdigit() else prev_str
        nxt = int(nxt_str) if nxt_str.isdigit() else nxt_str

        if curr != "?":
            self.rec(ind + 1)
            return

        options: str

        err_info = f" - {prev=}, {nxt=}, {ind=}"

        match (prev, nxt):
            case "?", _:
                raise RuntimeError("Prev should never be ?" + err_info)
            case "x", "x":
                options = "987654321"
            case (int(), "x") if prev > 2:
                options = "987654321"
            case 2, "x":
                options = "6543210"
            case 1, "x":
                options = "9876543210"
            case 0, "x":
                options = "9876543210"
            case (_, int()) if nxt > 6:
                options = "1"
            case _, int():
                options = "21"
            case _, "?":
                options = "21"
            case _, _:
                raise RuntimeError("Unhandled case" + err_info)

        for option in options:
            self.e[ind] = option
            self.rec(ind + 1)
            self.e[ind] = "?"
            if self.done:
                return


@lru_cache(maxsize=1_000_000_000)
def rec_count(e: str, ind: int, prev: str) -> int:
    if ind == len(e):
        return 1
    if e[ind] == "0" and prev in ("1", "2"):
        return rec_count(e, ind + 1, prev + e[ind])
    if e[ind] == "0":
        return 0
    if prev == "1" or (prev == "2" and e[ind] in "0123456"):
        return rec_count(e, ind + 1, e[ind]) + rec_count(e, ind + 1, prev + e[ind])
    return rec_count(e, ind + 1, e[ind])


def solve(e: str, k: int) -> tuple[str, int]:
    solver = Solver(e=["x", *e, "x"], k=k)
    solver.rec(ind=1)
    final_e = "".join(solver.final_e[1:-1])

    # count = rec_count(final_e, 0, prev="")
    stack_list: list[tuple[int, str]] = [(0, "")]
    cache_dict: dict[tuple[int, str], int] = {}
    count = 0
    while stack_list:
        ind, prev = stack_list.pop()
        if ind == len(final_e):
            count += 1
            continue
        if (ind, prev) in cache_dict:
            count += cache_dict[(ind, prev)]
            continue
        if final_e[ind] == "0" and prev in ("1", "2"):
            stack_list.append((ind + 1, prev + final_e[ind]))
            continue
        if final_e[ind] == "0":
            cache_dict[(ind, prev)] = 0
            continue
        if prev == "1" or (prev == "2" and final_e[ind] in "0123456"):
            stack_list.append((ind + 1, final_e[ind]))
            stack_list.append((ind + 1, prev + final_e[ind]))
            continue
        stack_list.append((ind + 1, final_e[ind]))
        cache_dict[(ind, prev)] = 1
    return final_e, count


def main() -> None:
    sys.setrecursionlimit(2**31 - 1)
    T = int(input())
    for t in range(T):
        e, k_str = input().split()
        k = int(k_str)
        final_e, count = solve(e=e, k=k)
        print(f"Case #{t + 1}: {final_e} {count}", flush=True)


if __name__ == "__main__":
    main()
