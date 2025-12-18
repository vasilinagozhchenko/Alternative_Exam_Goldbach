import time
import math
import matplotlib.pyplot as plt
import numpy as np


def sieve_of_eratosthenes(max_n):
    is_prime = [True] * (max_n + 1)
    is_prime[0] = is_prime[1] = False

    limit = int(math.sqrt(max_n)) + 1
    for i in range(2, limit):
        if is_prime[i]:
            for j in range(i * i, max_n + 1, i):
                is_prime[j] = False
    return is_prime


def check_goldbach_sieve(max_N):
    start_time = time.time()

    is_prime = sieve_of_eratosthenes(max_N)

    for N in range(4, max_N + 1, 2):
        found = False

        for a in range(2, N // 2 + 1):
            b = N - a

            if is_prime[a] and is_prime[b]:
                found = True
                break

        if not found:
            return time.time() - start_time

    return time.time() - start_time


def check_goldbach_sieve_with_output(max_N):
    is_prime = sieve_of_eratosthenes(max_N)

    for N in range(4, max_N + 1, 2):
        found = False

        for a in range(2, N // 2 + 1):
            b = N - a

            if is_prime[a] and is_prime[b]:
                found = True
                break

        if not found:
            return False

    return True


max_N = 8000000
result = check_goldbach_sieve_with_output(max_N)

test_sizes = [500000, 1000000, 2000000, 3000000, 4000000,
              4500000, 5000000, 5500000, 6000000,
              6500000, 7000000, 8000000]
execution_times = []

for max_N in test_sizes:
    elapsed_time = check_goldbach_sieve(max_N)
    execution_times.append(elapsed_time)
    print(f"N = {max_N:8d}: {elapsed_time:7.2f} секунд")

n_array = np.array(test_sizes)
t_array = np.array(execution_times)

A = np.vstack([n_array**2, np.ones(len(n_array))]).T
k, b = np.linalg.lstsq(A, t_array, rcond=None)[0]

predicted = k * (n_array ** 2) + b
errors = np.abs(t_array - predicted)
relative_errors = errors / t_array * 100

n_smooth = np.linspace(min(test_sizes), max(test_sizes), 100)
t_theoretical = k * (n_smooth ** 2) + b


plt.figure(figsize=(12, 8))


plt.plot(test_sizes, execution_times, 'bo-', linewidth=3, markersize=10,
         label='Реальное время выполнения', markerfacecolor='blue',
         markeredgewidth=1, markeredgecolor='blue')

plt.plot(n_smooth, t_theoretical, 'r--', linewidth=3,
         label=f'Теоретическая O(n²)\nk = {k:.2e}')

plt.xlabel('Количество чисел (n)', fontsize=14)
plt.ylabel('Время выполнения (секунды)', fontsize=14)
plt.title('Проверка гипотезы Гольдбаха - оптимизация решето Эратосфена',
          fontsize=14, pad=20)
plt.legend(fontsize=12, loc='upper left')
plt.grid(True, alpha=0.3, linestyle='--')

for i, (x, y) in enumerate(zip(test_sizes, execution_times)):
    plt.annotate(f'{y:.1f}с', (x, y), textcoords="offset points",
                 xytext=(0, 12), ha='center', fontsize=10,
                )


plt.tight_layout()
plt.show()
