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


def check_goldbach_naive_for_graph(max_N):
    start_time = time.time()

    for N in range(4, max_N + 1, 2):
        found = False

        for a in range(2, N // 2 + 1):
            b = N - a

            if is_prime_naive(a) and is_prime_naive(b):
                found = True
                break

        if not found:
            return time.time() - start_time

    return time.time() - start_time


test_sizes = [2000, 3000, 4000, 5000, 6000, 8000, 10000]

execution_times = []

for max_N in test_sizes:
    elapsed_time = check_goldbach_naive_for_graph(max_N)
    execution_times.append(elapsed_time)


plt.figure(figsize=(10, 6))

plt.plot(test_sizes, execution_times, 'bo-', linewidth=2, markersize=8,
         label='Реальное время выполнения', markerfacecolor='blue')

n_array = np.array(test_sizes)
t_array = np.array(execution_times)

k_values = t_array / (n_array ** 3)
k = np.mean(k_values)

n_theoretical = np.linspace(min(test_sizes), max(test_sizes), 100)
t_theoretical = k * (n_theoretical ** 3)

plt.plot(n_theoretical, t_theoretical, 'r--', linewidth=2,
         label=f'Теоретическое O(n³)')

plt.xlabel('Количество чисел', fontsize=12)
plt.ylabel('Время выполнения (секунды)', fontsize=12)
plt.title('Проверка гипотезы Гольдбаха - половинный перебор', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)

for i, (x, y) in enumerate(zip(test_sizes, execution_times)):
    plt.annotate(f'{y:.2f}с', (x, y), textcoords="offset points",
                 xytext=(0, 10), ha='center', fontsize=9)

plt.tight_layout()
plt.show()
