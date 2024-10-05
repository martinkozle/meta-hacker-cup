def main() -> None:
    T = int(input())
    for t in range(T):
        N = int(input())
        min_speed = -1.0
        max_speed: float = 2**128
        for n in range(N):
            a, b = map(float, input().split())
            a = max(a, 0.000000001)
            min_speed = max(min_speed, (n + 1) / b)
            max_speed = min(max_speed, (n + 1) / a)
        if max_speed < min_speed:
            min_speed = -1
        print(f"Case #{t + 1}: {min_speed}")


if __name__ == "__main__":
    main()
