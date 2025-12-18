import time
import math
import bisect


def find_goldbach_numbers(max_N):
    start_time = time.time()
    is_prime = [True] * (max_N + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(math.sqrt(max_N)) + 1):
        if is_prime[i]:
            for j in range(i * i, max_N + 1, i):
                is_prime[j] = False

    can_be_goldbach = [False] * (max_N + 1)

    primes = [i for i in range(2, max_N + 1) if is_prime[i]]

    for i, a in enumerate(primes):
        max_b = max_N - a
        j_max = bisect.bisect_right(primes, max_b) - 1
        if j_max >= i:
            for j in range(i, j_max + 1):
                b = primes[j]
                sum_primes = a + b
                if sum_primes % 2 == 0:
                    can_be_goldbach[sum_primes] = True

    all_found = True

    for N in range(4, max_N + 1, 2):
        if not can_be_goldbach[N]:
            all_found = False
            break

    end_time = time.time()

    print(f"Проверка завершена за {end_time - start_time:.2f} сек")

    if all_found:
        print(f"Гипотеза Гольдбаха верна для всех N от 4 до {max_N}")
    else:
        print(f"Ошибка. Гипотеза неверна для N = {N}")

    return all_found


if __name__ == "__main__":
    print("Проверка гипотезы Гольдбаха:")
    max_N = 50000
    result = find_goldbach_numbers(max_N)