import time


def sieve_of_eratosthenes(max_n):
    is_prime = [True] * (max_n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, max_n + 1):
        if is_prime[i]:
            for j in range(i * i, max_n + 1, i):
                is_prime[j] = False
    return is_prime


def check_goldbach_sieve_cache(max_N):
    start_time = time.time()

    is_prime = sieve_of_eratosthenes(max_N)

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
            result = is_prime[n]
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
    result = check_goldbach_sieve_cache(max_N)