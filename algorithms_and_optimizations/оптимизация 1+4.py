import time
import math


def is_prime_sqrt(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def check_goldbach_sqrt_cache(max_N):
    start_time = time.time()

    prime_cache = {}
    cache_hits = 0
    cache_misses = 0

    def is_prime_cached(n):
        nonlocal cache_hits, cache_misses
        if n in prime_cache:
            cache_hits += 1
            return prime_cache[n]
        else:
            cache_misses += 1
            result = is_prime_sqrt(n)
            prime_cache[n] = result
            return result

    for N in range(4, max_N + 1, 2):
        found = False

        for a in range(2, N):
            b = N - a
            if is_prime_cached(a) and is_prime_cached(b):
                found = True
                break

        if not found:
            print(f"Ошибка. Гипотеза неверна для N = {N}")
            return False

    end_time = time.time()
    print(f"Гипотеза Гольдбаха верна для всех N от 4 до {max_N}")
    print(f"Время выполнения: {end_time - start_time:.2f} сек")
    return True


if __name__ == "__main__":
    print("Проверка гипотезы Гольдбаха:")
    max_N = 50000
    result = check_goldbach_sqrt_cache(max_N)