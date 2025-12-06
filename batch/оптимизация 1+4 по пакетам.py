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


def batch(max_N):
    start_time = time.time()

    batch_size = 1000
    batch_count = 0
    total_checked = 0
    batch_start_time = time.time()

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

    print("Пакет | Обработано чисел | Скорость (чисел/сек) | Текущее N")
    print("-" * 65)

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

        batch_count += 1
        total_checked += 1

        if batch_count >= batch_size:
            batch_end_time = time.time()
            batch_time = batch_end_time - batch_start_time
            speed = batch_size / batch_time if batch_time > 0 else 0
            print(
                f"{total_checked // batch_size:5}  {total_checked:15}  {speed:18.1f}  {N:9}")
            batch_count = 0
            batch_start_time = time.time()

    if batch_count > 0:
        batch_end_time = time.time()
        batch_time = batch_end_time - batch_start_time
        speed = batch_count / batch_time if batch_time > 0 else 0
        print(
            f"{total_checked // batch_size + 1:5}  {total_checked:15}  {speed:18.1f}  {max_N:9}")

    end_time = time.time()
    total_time = end_time - start_time
    avg_speed = total_checked / total_time if total_time > 0 else 0

    print("-" * 65)
    print(f"\nГипотеза Гольдбаха верна для всех N от 4 до {max_N}")
    print(f"Общее время: {total_time:.4f} сек")
    print(f"Средняя скорость: {avg_speed:.1f} чисел/сек")

    return True


if __name__ == "__main__":
    print("Проверка гипотезы Гольдбаха (Корень + Кэширование):")
    max_N = 50000
    result = batch(max_N)