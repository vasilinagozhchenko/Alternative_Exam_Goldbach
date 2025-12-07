import time
import math
import matplotlib.pyplot as plt
import numpy as np


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


def check_goldbach_optimized_for_graph(max_N):
    start_time = time.time()

    for N in range(4, max_N + 1, 2):
        found = False

        for a in range(2, N):
            b = N - a

            if optim1(a) and optim1(b):
                found = True
                break

        if not found:
            return time.time() - start_time

    return time.time() - start_time


def check_goldbach_optimized(max_N):
    for N in range(4, max_N + 1, 2):
        found = False

        for a in range(2, N):
            b = N - a

            if optim1(a) and optim1(b):
                found = True
                break

        if not found:
            return False

    return True


max_N = 50000
result = check_goldbach_optimized(max_N)

test_sizes = [2000, 3000, 4000, 5000, 6000, 8000, 10000]
execution_times = []

for max_N in test_sizes:
    elapsed_time = check_goldbach_optimized_for_graph(max_N)
    execution_times.append(elapsed_time)

n_array = np.array(test_sizes)
t_array = np.array(execution_times)

plt.figure(figsize=(10, 6))

plt.plot(test_sizes, execution_times, 'bo-', linewidth=2, markersize=8,
         label='Реальное время выполнения', markerfacecolor='blue')

sqrt_n = np.sqrt(n_array)
n_squared = n_array ** 2
k_values = t_array / (sqrt_n * n_squared)
k = np.mean(k_values)

n_smooth = np.linspace(min(test_sizes), max(test_sizes), 100)
t_theoretical = k * (np.sqrt(n_smooth) * (n_smooth ** 2))

plt.plot(n_smooth, t_theoretical, 'r--', linewidth=2,
         label=f'Теоретическая O(n²√n)')

plt.xlabel('Количество чисел', fontsize=12)
plt.ylabel('Время выполнения (секунды)', fontsize=12)
plt.title('Проверка гипотезы Гольдбаха с корнем', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)

for i, (x, y) in enumerate(zip(test_sizes, execution_times)):
    plt.annotate(f'{y:.2f}с', (x, y), textcoords="offset points",
                 xytext=(0, 10), ha='center', fontsize=9)

plt.tight_layout()
plt.show()
