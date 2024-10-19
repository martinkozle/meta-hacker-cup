def main() -> None:
    T = int(input())
    all_peaks: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for num_digits in (3, 5, 7, 9, 11, 13, 15, 17, 19, 21):
        for start in range(1, 10 - num_digits // 2):
            half_peak = "".join(map(str, range(start, start + num_digits // 2)))
            peak = int(half_peak + str(start + num_digits // 2) + half_peak[::-1])
            all_peaks.append(peak)

    for t in range(T):
        A, B, M = map(int, input().split())
        compatible_peaks = [
            peak for peak in all_peaks if A <= peak <= B and peak % M == 0
        ]
        print(f"Case #{t+1}: {len(compatible_peaks)}")


if __name__ == "__main__":
    main()
