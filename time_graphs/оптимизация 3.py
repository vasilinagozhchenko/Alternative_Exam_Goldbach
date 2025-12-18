import time
import matplotlib.pyplot as plt
import numpy as np


def is_prime_naive(n):
    if n < 2:
        return False
    for i in range(2, n): 
        if n % i == 0:
            return False
    return True


def check_goldbach_sequential_timing(max_N):
    start_time = time.perf_counter()
    for N in range(4, max_N + 1, 2):
        found = False
        for a in range(2, N):
            b = N - a
            if is_prime_naive(a) and is_prime_naive(b):
                found = True
                break
        if not found:
            return time.perf_counter() - start_time
    return time.perf_counter() - start_time


def main():
    test_sizes = [10000, 20000, 30000, 40000, 50000]
    seq_times = []
    for max_N in test_sizes:
        t = check_goldbach_sequential_timing(max_N)
        seq_times.append(t)
        print(f"max_N={max_N}, t={t:.2f}с")

    n_array = np.array(test_sizes)
    t_array = np.array(seq_times)

    k_values = t_array / (n_array ** 3)
    k = np.mean(k_values)

    n_smooth = np.linspace(min(test_sizes), max(test_sizes), 200)
    t_theoretical = k * (n_smooth ** 3)

    plt.figure(figsize=(10, 6))

    plt.plot(test_sizes, seq_times, 'bo-', linewidth=2.5, markersize=8,
             label='Экспериментальное время', markerfacecolor='blue')

    plt.plot(n_smooth, t_theoretical, 'r--', linewidth=3,
             label=f'Теоретическая O(n³)\nk = {k:.2e}')

    plt.xlabel('Количество чисел', fontsize=13)
    plt.ylabel('Время выполнения (секунды)', fontsize=13)
    plt.title('Проверка гипотезы Гольдбаха - параллелизация', fontsize=14, pad=15)
    plt.legend(fontsize=12, loc='upper left')
    plt.grid(True, alpha=0.3)

    for x, y in zip(test_sizes, seq_times):
        plt.annotate(f'{y:.1f}с', (x, y), textcoords="offset points",
                     xytext=(0, 10), ha='center', fontsize=10, color='black')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()