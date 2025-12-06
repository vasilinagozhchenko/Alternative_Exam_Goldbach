import time
from multiprocessing import Pool, cpu_count


def sieve_of_eratosthenes(max_n):
    is_prime = [True] * (max_n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, max_n + 1):
        if is_prime[i]:
            for j in range(i * i, max_n + 1, i):
                is_prime[j] = False
    return is_prime


def check_goldbach_range(args):
    start, end, is_prime = args

    for N in range(start, end + 1, 2):
        found = False
        for a in range(2, N):
            b = N - a
            if is_prime[a] and is_prime[b]:
                found = True
                break
        if not found:
            return (False, N)
    return (True, None)


def check_goldbach_sieve_parallel(max_N):
    start_time = time.time()

    is_prime = sieve_of_eratosthenes(max_N)

    num = cpu_count()
    even_numbers = list(range(4, max_N + 1, 2))
    chunk_size = len(even_numbers) // num

    ranges = []
    for i in range(num):
        start_index = i * chunk_size
        if i == num - 1:
            end_index = len(even_numbers) - 1
        else:
            end_index = start_index + chunk_size - 1

        start_N = even_numbers[start_index]
        end_N = even_numbers[end_index]
        ranges.append((start_N, end_N, is_prime))

    print(f"Запускаем {num} процессов для проверки диапазонов...")

    with Pool(num) as pool:
        results = pool.map(check_goldbach_range, ranges)

    all_valid = True

    for result in results:
        is_valid, data = result
        if not is_valid:
            all_valid = False
            break

    end_time = time.time()
    print(f"Гипотеза Гольдбаха верна для всех N от 4 до {max_N}")
    print(f"Время выполнения: {end_time - start_time:.2f} сек")
    return all_valid


if __name__ == "__main__":
    print("Проверка гипотезы Гольдбаха:")
    max_N = 50000
    result = check_goldbach_sieve_parallel(max_N)