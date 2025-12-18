import time
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


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


test_sizes = [100000, 200000, 500000, 1000000, 1500000, 2000000, 2500000, 3000000, 4000000]
execution_times = []
for max_N in test_sizes:
    elapsed_time = check_goldbach_optimized_for_graph(max_N)
    execution_times.append(elapsed_time)

n_array = np.array(test_sizes)
t_array = np.array(execution_times)


def theoretical_func(x, k, c):
    return k * (x ** 2.5) + c


try:
    params, covariance = curve_fit(theoretical_func, n_array, t_array)
    k_optimal, c_optimal = params
    n_smooth = np.linspace(min(test_sizes), max(test_sizes), 500)
    t_theoretical_optimal = theoretical_func(n_smooth, k_optimal, c_optimal)

    fit_success = True
except Exception as e:
    fit_success = False

plt.figure(figsize=(12, 8))

plt.plot(test_sizes, execution_times, 'bo-', linewidth=3, markersize=10,
         label='Реальное время выполнения', markerfacecolor='blue', markeredgecolor='black')

if fit_success:
    plt.plot(n_smooth, t_theoretical_optimal, 'r--', linewidth=3,
             label=f'Теоретическая O(n²√n) \nk = {k_optimal:.2e}')

n_squared_sqrt = n_array ** 2 * np.sqrt(n_array)
k_simple = np.mean(t_array / n_squared_sqrt)

n_smooth = np.linspace(min(test_sizes), max(test_sizes), 500)
t_theoretical_simple = k_simple * (n_smooth ** 2 * np.sqrt(n_smooth))

plt.xlabel('Количество чисел', fontsize=14)
plt.ylabel('Время выполнения (секунды)', fontsize=14)
plt.title('Проверка гипотезы Гольдбаха - проход до корня', fontsize=16)
plt.legend()
plt.grid(True, alpha=0.3)

for i, (x, y) in enumerate(zip(test_sizes, execution_times)):
    plt.annotate(f'{y:.2f}с', (x, y), textcoords="offset points",
                 xytext=(0, 10), ha='center', fontsize=10, weight='bold')

plt.tight_layout()
plt.show()
