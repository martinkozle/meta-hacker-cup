from itertools import combinations_with_replacement


def main() -> None:
    CREATE_PRECOMPUTE_CACHE = False

    if CREATE_PRECOMPUTE_CACHE:
        all_mountains: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for num_digits in (3, 5, 7, 9, 11, 13, 15, 17):
            print(num_digits)
            all_non_decreasing_sequences = list(
                combinations_with_replacement(range(1, 9), num_digits // 2)
            )
            all_non_increasing_sequences = [
                seq[::-1] for seq in all_non_decreasing_sequences
            ]
            for first_seq in all_non_decreasing_sequences:
                for second_seq in all_non_increasing_sequences:
                    for middle in range(max(first_seq[-1], second_seq[0]) + 1, 10):
                        all_mountains.append(
                            int(
                                f"{"".join(map(str, first_seq))}{middle}{"".join(map(str, second_seq))}"
                            )
                        )

        print("Total number of mountains:", len(all_mountains))
        print("Sorting mountains...")
        all_mountains.sort()

        print("Writing cache...")
        with open("a2_cache.txt", "w") as f:
            f.writelines(str(mountain) + "\n" for mountain in all_mountains)

        return
    else:
        with open("a2_cache.txt") as f:
            all_mountains = [int(line.strip()) for line in f.readlines() if line != ""]

    T = int(input())
    for t in range(T):
        A, B, M = map(int, input().split())
        compatible_peaks = [
            mountain
            for mountain in all_mountains
            if A <= mountain <= B and mountain % M == 0
        ]
        print(f"Case #{t+1}: {len(compatible_peaks)}")


if __name__ == "__main__":
    main()
