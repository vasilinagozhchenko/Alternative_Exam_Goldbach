import time
import math


def interpolation_search_primes(arr, x):
    if not arr or x < arr[0]:
        return -1
    if x > arr[-1]:
        return len(arr) - 1

    low = 0
    high = len(arr) - 1

    while low <= high and x >= arr[low] and x <= arr[high]:
        if low == high:
            return low if arr[low] <= x else low - 1

        v_low = arr[low]
        v_high = arr[high]
        if v_high - v_low < 2:
            pos = low
        else:
            def approx_pi(v):
                return v / math.log(v) if v > 1 else 0

            pi_x = approx_pi(x)
            pi_low = approx_pi(v_low)
            pi_high = approx_pi(v_high)

            if pi_high != pi_low:
                ratio = (pi_x - pi_low) / (pi_high - pi_low)
                pos = low + int(ratio * (high - low))
            else:
                pos = low

        pos = max(low, min(pos, high))

        if arr[pos] == x:
            while pos < len(arr) - 1 and arr[pos + 1] == x:
                pos += 1
            return pos

        if arr[pos] < x:
            low = pos + 1
        else:
            high = pos - 1

    return high


def find_goldbach_numbers(max_N):
    start_time = time.time()

    is_prime = [True] * (max_N + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.sqrt(max_N)) + 1):
        if is_prime[i]:
            for j in range(i * i, max_N + 1, i):
                is_prime[j] = False

    primes = [i for i in range(2, max_N + 1) if is_prime[i]]

    if not primes:
        return False

    can_be_goldbach = [False] * (max_N + 1)

    for i, a in enumerate(primes):
        max_b = max_N - a
        if max_b < a:
            break

        j_max = interpolation_search_primes(primes, max_b)

        for j in range(i, j_max + 1):
            b = primes[j]
            sum_primes = a + b
            if sum_primes <= max_N:
                can_be_goldbach[sum_primes] = True

    all_found = True
    for N in range(4, max_N + 1, 2):
        if not can_be_goldbach[N]:
            all_found = False
            print(f"Ошибка. Гипотеза неверна для N = {N}")
            break

    end_time = time.time()
    print(f"Проверка завершена за {end_time - start_time:.4f} сек")

    if all_found:
        print(f"Гипотеза Гольдбаха верна для всех четных N до {max_N}")

    return all_found


if __name__ == "__main__":
    max_N = 50000
    find_goldbach_numbers(max_N)
