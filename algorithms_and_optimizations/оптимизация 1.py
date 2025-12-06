import time
import math


def optim1(n):
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


def check_goldbach_optimized(max_N):
    start_time = time.time()

    for N in range(4, max_N + 1, 2):
        found = False

        for a in range(2, N):
            b = N - a

            if optim1(a) and optim1(b):
                found = True
                break

        if not found:
            print(f"Ошибка. Гипотеза неверна для N = {N}")
            return False

    end_time = time.time()
    print(f"Гипотеза Гольдбаха верна для всех N от 4 до {max_N}")
    print(f"Время выполнения: {end_time - start_time:.2f} секунд")
    return True


if __name__ == "__main__":
    print("Проверка гипотезы Гольдбаха:")
    max_N = 50000
    result = check_goldbach_optimized(max_N)