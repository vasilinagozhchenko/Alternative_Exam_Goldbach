import time
import math
from multiprocessing import Pool, cpu_count


def is_prime_naive(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def batch(args):
    start, end, process_id = args
    results = []

    batch_size = 500
    batch_count = 0
    total_checked_in_process = 0
    batch_start_time = time.time()

    for N in range(start, end + 1, 2):
        found = False
        for a in range(2, N):
            b = N - a
            if is_prime_naive(a) and is_prime_naive(b):
                found = True
                break
        if not found:
            return (False, N, process_id)
        results.append((N, a, b))

        batch_count += 1
        total_checked_in_process += 1

        if batch_count >= batch_size:
            batch_end_time = time.time()
            batch_time = batch_end_time - batch_start_time
            speed = batch_size / batch_time if batch_time > 0 else 0

            print(f"Процесс {process_id}: пакет {total_checked_in_process // batch_size}  "
                  f"скорость {speed:6.1f} чисел/сек  N={N}")

            batch_count = 0
            batch_start_time = time.time()

    if batch_count > 0:
        batch_end_time = time.time()
        batch_time = batch_end_time - batch_start_time
        speed = batch_count / batch_time if batch_time > 0 else 0
        print(f"Процесс {process_id}: пакет {total_checked_in_process // batch_size + 1}  "
              f"скорость {speed:6.1f} чисел/сек  N={end}")

    return (True, results, process_id, total_checked_in_process)


def check_goldbach_parallel(max_N, num_processes=None):
    start_time = time.time()

    if num_processes is None:
        num_processes = cpu_count()

    print(f"Запуск параллельной проверки на {num_processes} процессах")
    even_numbers = list(range(4, max_N + 1, 2))
    chunk_size = len(even_numbers) // num_processes

    ranges = []
    for i in range(num_processes):
        start_index = i * chunk_size
        if i == num_processes - 1:
            end_index = len(even_numbers) - 1
        else:
            end_index = start_index + chunk_size - 1

        start_N = even_numbers[start_index]
        end_N = even_numbers[end_index]
        ranges.append((start_N, end_N, i))

    print(f"Диапазоны для процессов: {[f'{r[0]}-{r[1]}' for r in ranges]}")
    print()

    with Pool(num_processes) as pool:
        results = pool.map(batch, ranges)

    all_valid = True
    counterexample = None
    total_checked = 0

    print("\n" + "=" * 70)

    for result in results:
        is_valid, data, process_id, checked_in_process = result
        total_checked += checked_in_process

    end_time = time.time()
    total_time = end_time - start_time
    avg_speed = total_checked / total_time if total_time > 0 else 0

    if all_valid:
        print(f"\nГипотеза Гольдбаха верна для всех N от 4 до {max_N}")
        print(f"Общее время: {total_time:.2f} секунд")
        print(f"Использовано процессов: {num_processes}")
        print(f"Средняя скорость: {avg_speed:.1f} чисел/сек")
        return True
    else:
        print(f"\nОшибка. Гипотеза неверна для N = {counterexample}")
        print(f"Время выполнения: {total_time:.2f} секунд")
        return False


if __name__ == "__main__":
    max_N = 50000
    result = check_goldbach_parallel(max_N)