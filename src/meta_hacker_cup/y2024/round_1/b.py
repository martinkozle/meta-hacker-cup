import math


def prime_sieve(max_n: int) -> list[int]:
    sieve = [True] * (max_n // 2 + 2)
    for i in range(3, int(math.sqrt(max_n)) + 1, 2):
        if sieve[i >> 1]:
            for j in range(i**2, max_n + 1, 2 * i):
                sieve[j >> 1] = False
    primes = [2]
    for i in range(3, max_n + 1, 2):
        if sieve[i >> 1]:
            primes.append(i)
    return primes


def binary_find(n: int, arr: list[int]) -> int:
    minim = 0
    maxim = len(arr) - 1
    while minim < maxim:
        ind = (maxim + minim) // 2
        # print(minim, maxim, ind)
        if arr[ind - 1] <= n < arr[ind]:
            return ind
        if arr[ind] <= n:
            minim = ind
        else:
            maxim = ind
    return minim


def main() -> None:
    T = int(input())
    n_list: list[int] = [int(input()) for _ in range(T)]
    max_n = max(n_list)
    primes = prime_sieve(max_n=max_n + 1000)
    primes_set = set(primes)
    sm = [5, *(prime + 2 for prime in primes if prime + 2 in primes_set)]

    for t, n in enumerate(n_list):
        ind = binary_find(n, sm)
        print(f"Case #{t + 1}: {ind}")


if __name__ == "__main__":
    main()
