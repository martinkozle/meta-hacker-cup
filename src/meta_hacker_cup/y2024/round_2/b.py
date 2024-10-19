from concurrent.futures import Future, ProcessPoolExecutor


def board_to_str(board: list[list[str]]) -> str:
    return "\n".join("".join(column) for column in board)


def str_to_board(board_str: str) -> list[list[str]]:
    return [list(column) for column in board_str.split("\n")]


def switch_turn(turn: str) -> str:
    return "C" if turn == "F" else "F"


def merge_winner(prev_winner: str, curr_winner: str) -> str:
    match (prev_winner, curr_winner):
        case ("0", _):
            return curr_winner
        case ("?", _):
            return "?"
        case ("C", "F"):
            return "?"
        case ("C", "?"):
            return "?"
        case ("C", _):
            return "C"
        case ("F", "C"):
            return "?"
        case ("F", "?"):
            return "?"
        case ("F", _):
            return "F"
        case _:
            raise ValueError(f"Invalid winners {prev_winner}, {curr_winner}")


def check_winner(board: list[list[str]]) -> str:
    winner: str = "0"
    for column in board:
        if "CCCC" in "".join(column):
            winner = merge_winner(winner, "C")
        if "FFFF" in "".join(column):
            winner = merge_winner(winner, "F")
    for row_ind in range(6):
        row = [
            board[col_ind][row_ind] if len(board[col_ind]) > row_ind else " "
            for col_ind in range(7)
        ]
        if "CCCC" in "".join(row):
            winner = merge_winner(winner, "C")
        if "FFFF" in "".join(row):
            winner = merge_winner(winner, "F")
    for start_col_ind in range(7):
        for start_row_ind in range(6):
            diag_list: list[str] = []
            for dist in range(10):
                if start_col_ind + dist >= 7 or start_row_ind + dist >= len(
                    board[start_col_ind + dist]
                ):
                    break
                diag_list.append(
                    (board[start_col_ind + dist] + [" "] * 10)[start_row_ind + dist]
                )
            diag = "".join(diag_list)
            diag_list = []
            if "CCCC" in "".join(diag):
                winner = merge_winner(winner, "C")
            if "FFFF" in "".join(diag):
                winner = merge_winner(winner, "F")
            for dist in range(10):
                if start_col_ind + dist >= 7 or start_row_ind - dist < 0:
                    break
                diag_list.append(
                    (board[start_col_ind + dist] + [" "] * 10)[start_row_ind - dist]
                )
            diag = "".join(diag_list)
            if "CCCC" in "".join(diag):
                winner = merge_winner(winner, "C")
            if "FFFF" in "".join(diag):
                winner = merge_winner(winner, "F")
    return winner


def solve(final_board: list[list[str]]) -> str:
    merged_winner: str = "0"
    visited: set[tuple[str, str]] = set()
    stack: list[tuple[str, str]] = [("\n\n\n\n\n\n", "C")]
    while len(stack) > 0:
        board_str, next_turn = stack.pop()
        if (board_str, next_turn) in visited:
            continue
        board = str_to_board(board_str)
        winner = check_winner(board)
        visited.add((board_str, next_turn))
        if winner in "CF?":
            merged_winner = merge_winner(merged_winner, winner)
            continue
        if all(len(column) == 6 for column in board):
            continue
        for c, column in enumerate(board):
            if len(column) < 6 and final_board[c][len(column)] == next_turn:
                column.append(next_turn)
                stack.append((board_to_str(board), switch_turn(next_turn)))
                column.pop()
    return merged_winner


def main() -> None:
    MAX_WORKERS = 100
    T = int(input())

    with ProcessPoolExecutor(MAX_WORKERS) as pool:
        futures: list[Future[str]] = []
        for t in range(T):
            input()
            final_board_by_rows = [input().strip() for _ in range(6)]
            final_board = [
                [final_board_by_rows[row_ind][column_ind] for row_ind in range(6)][::-1]
                for column_ind in range(7)
            ]
            futures.append(pool.submit(solve, final_board))
        for t, future in enumerate(futures):
            winner = future.result()
            print(f"Case #{t+1}: {winner}")


if __name__ == "__main__":
    main()
