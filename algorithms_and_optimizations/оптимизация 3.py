import time
from multiprocessing import Pool, cpu_count


def is_prime_naive(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def check_goldbach_range(args):
    start, end = args
    results = []

    for N in range(start, end + 1, 2):
        found = False
        for a in range(2, N):
            b = N - a
            if is_prime_naive(a) and is_prime_naive(b):
                found = True
                break
        if not found:
            return (False, N)
        results.append((N, a, b))

    return (True, results)


def check_goldbach_parallel(max_N, num_processes=None):
    start_time = time.time()

    if num_processes is None:
        num_processes = cpu_count()

    print(f"Запуск параллельной проверки на {num_processes} процессах")

    num = list(range(4, max_N + 1, 2))
    size = len(num) // num_processes

    ranges = []
    for i in range(num_processes):
        start_index = i * size
        if i == num_processes - 1:
            end_index = len(num) - 1
        else:
            end_index = start_index + size - 1

        start_N = num[start_index]
        end_N = num[end_index]
        ranges.append((start_N, end_N))

    print(f"Диапазоны для процессов: {ranges}")

    with Pool(num_processes) as pool:
        results = pool.map(check_goldbach_range, ranges)

    all_valid = True
    counterexample = None

    for result in results:
        is_valid, data = result
        if not is_valid:
            all_valid = False
            counterexample = data
            break

    end_time = time.time()

    if all_valid:
        print(f"\nГипотеза Гольдбаха верна для всех N от 4 до {max_N}")
        print(f"Время выполнения: {end_time - start_time:.2f} секунд")
        print(f"Использовано процессов: {num_processes}")
        return True
    else:
        print(f"\nОшибка. Гипотеза неверна для N = {counterexample}")
        return False


if __name__ == "__main__":
    max_N = 50000
    result = check_goldbach_parallel(max_N)