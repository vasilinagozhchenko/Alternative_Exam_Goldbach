import time


def is_prime_naive(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def check_goldbach_continuous():
    print("Программа будет проверять все четные числа начиная с 4")
    print("=" * 50)

    start_time = time.time()
    N = 4
    checked_count = 0
    last_report_time = time.time()

    try:
        while True:
            found = False

            for a in range(2, N):
                b = N - a
                if is_prime_naive(a) and is_prime_naive(b):
                    found = True
                    break

            if not found:
                print(f"Ошибка. Гипотеза неверна для N = {N}")
                print(f"Программа проверяла {checked_count} чисел за {time.time() - start_time:.2f} секунд")
                return False

            checked_count += 1

            current_time = time.time()
            if current_time - last_report_time >= 5:
                elapsed = current_time - start_time
                speed = checked_count / elapsed if elapsed > 0 else 0
                print(f"Проверено: {checked_count} чисел | Текущее N: {N} | "
                      f"Скорость: {speed:.2f} чисел/сек | Время: {elapsed:.1f} сек")
                last_report_time = current_time

            N += 2

    except KeyboardInterrupt:
        elapsed = time.time() - start_time
        print(f"Программа остановлена пользователем")
        print(f"Проверено {checked_count} четных чисел")
        print(f"Последнее проверенное число: {N - 2}")
        print(f"Общее время работы: {elapsed:.2f} секунд")
        print(f"Средняя скорость: {checked_count / elapsed:.2f} чисел/сек")
        return True


if __name__ == "__main__":
    print("Запуск непрерывной проверки гипотезы Гольдбаха...")
    time.sleep(2)
    result = check_goldbach_continuous()
    if result:
        print("Гипотеза верна для всех проверенных чисел")
    else:
        print("Обнаружено нарушение гипотезы!")