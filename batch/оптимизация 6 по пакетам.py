import time


def is_prime_naive(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def batch(max_N):
    start_time = time.time()

    batch_size = 1000
    batch_count = 0
    total_checked = 0
    batch_start_time = time.time()

    print("Пакет | Обработано чисел | Скорость (чисел/сек) | Текущее N")
    print("-" * 65)

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

        batch_count += 1
        total_checked += 1

        if batch_count >= batch_size:
            batch_end_time = time.time()
            batch_time = batch_end_time - batch_start_time
            speed = batch_size / batch_time if batch_time > 0 else 0

            print(f"{total_checked // batch_size:5} | {total_checked:15} | {speed:18.1f} | {N:9}")

            batch_count = 0
            batch_start_time = time.time()

    if batch_count > 0:
        batch_end_time = time.time()
        batch_time = batch_end_time - batch_start_time
        speed = batch_count / batch_time if batch_time > 0 else 0
        print(f"{total_checked // batch_size + 1:5} | {total_checked:15} | {speed:18.1f} | {max_N:9}")

    end_time = time.time()
    total_time = end_time - start_time
    avg_speed = total_checked / total_time if total_time > 0 else 0

    print("-" * 65)
    print(f"Гипотеза верна для всех N от 4 до {max_N}")
    print(f"Общее время: {total_time:.2f} секунд")
    print(f"Средняя скорость: {avg_speed:.1f} чисел/сек")
    return True


if __name__ == "__main__":
    print("Оптимизация симметрии (проверка до N/2)")
    max_N = 50000
    result = batch(max_N)