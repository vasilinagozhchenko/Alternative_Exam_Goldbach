import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


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

        for a in range(2, N):
            b = N - a

            if is_prime_naive(a) and is_prime_naive(b):
                found = True
                break

        if not found:
            return time.time() - start_time

    return time.time() - start_time


test_sizes = [2000, 5000, 8000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000]

execution_times = []

for max_N in test_sizes:
    elapsed_time = check_goldbach_naive_for_graph(max_N)
    execution_times.append(elapsed_time)


def cubic_func(x, k, c):
    return k * x ** 3 + c


n_array = np.array(test_sizes)
t_array = np.array(execution_times)

params, _ = curve_fit(cubic_func, n_array, t_array)
k_fitted, c_fitted = params

print(f"Оптимальные параметры модели:")
print(f"k = {k_fitted:.10e}")
print(f"c = {c_fitted:.10f}")
print(f"c = {c_fitted} (полная точность)")

plt.figure(figsize=(12, 8))

plt.plot(test_sizes, execution_times, 'bo-', linewidth=3, markersize=10,
         label='Реальное время выполнения', markerfacecolor='blue', markeredgecolor='black')

n_theoretical = np.linspace(min(test_sizes), max(test_sizes), 500)
t_theoretical_fitted = cubic_func(n_theoretical, k_fitted, c_fitted)

plt.plot(n_theoretical, t_theoretical_fitted, 'r--', linewidth=3,
         label=f'Теоретическое O(n³) \n k = {k_fitted:.2e}')

k_scale = np.mean(t_array / (n_array ** 3))
t_simple_cubic = k_scale * (n_theoretical ** 3)

plt.xlabel('Количество чисел', fontsize=14)
plt.ylabel('Время выполнения (секунды)', fontsize=14)
plt.title('Проверка гипотезы Гольдбаха - тривиальный алгоритм', fontsize=16)
plt.legend()
plt.grid(True, alpha=0.3)

for i, (x, y) in enumerate(zip(test_sizes, execution_times)):
    plt.annotate(f'{y:.2f}с', (x, y), textcoords="offset points",
                 xytext=(0, 10), ha='center', fontsize=10, weight='bold')

plt.tight_layout()
plt.show()
