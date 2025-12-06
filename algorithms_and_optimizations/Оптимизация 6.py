import time


def is_prime_naive(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def check_goldbach_naive(max_N):
    start_time = time.time()
    for N in range(4, max_N + 1, 2):
        found = False
        for a in range(2, N // 2 + 1):
            b = N - a
            if is_prime_naive(a) and is_prime_naive(b):
                found = True
                break

        if not found:
            print(f"Ошибка. Гипотеза неверна для N = {N}")
            return False

    end_time = time.time()
    print(f"\nГипотеза Гольдбаха верна для всех N от 4 до {max_N}")
    print(f"Время выполнения: {end_time - start_time:.2f} секунд")
    return True


if __name__ == "__main__":
    print("Проверка гипотезы Гольдбаха:\n")
    max_N = 50000
    result = check_goldbach_naive(max_N)