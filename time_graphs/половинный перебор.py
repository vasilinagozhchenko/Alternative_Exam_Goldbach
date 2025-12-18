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


def check_goldbach_trivial(max_N):
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


def check_goldbach_half_optimized(max_N):
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


test_sizes = [20000, 50000, 60000, 80000, 100000]
execution_times_trivial = []
for max_N in test_sizes:
    elapsed_time = check_goldbach_trivial(max_N)
    execution_times_trivial.append(elapsed_time)
    
execution_times_half = []
for max_N in test_sizes:
    elapsed_time = check_goldbach_half_optimized(max_N)
    execution_times_half.append(elapsed_time)
    
plt.figure(figsize=(10, 6))

plt.plot(test_sizes, execution_times_trivial, 'bo-', linewidth=2, markersize=8,
         label='Тривиальный алгоритм (полный перебор)', markerfacecolor='blue')

plt.plot(test_sizes, execution_times_half, 'go-', linewidth=2, markersize=8,
         label='Оптимизированный алгоритм (половинный перебор)', markerfacecolor='green')


def cubic_func(x, k, c):
    return k * (x ** 3) + c


n_array_trivial = np.array(test_sizes)
t_array_trivial = np.array(execution_times_trivial)
params_trivial, _ = curve_fit(cubic_func, n_array_trivial, t_array_trivial)
k_trivial, c_trivial = params_trivial

n_array_half = np.array(test_sizes)
t_array_half = np.array(execution_times_half)
params_half, _ = curve_fit(cubic_func, n_array_half, t_array_half)
k_half, c_half = params_half

n_theoretical = np.linspace(min(test_sizes), max(test_sizes), 500)
t_theoretical_trivial = cubic_func(n_theoretical, k_trivial, c_trivial)

t_theoretical_half = cubic_func(n_theoretical, k_half, c_half)

plt.plot(n_theoretical, t_theoretical_trivial, 'r--', linewidth=2,
         label=f'Теоретическое O(n³) (k₁={k_trivial:.2e}, k₂={k_half:.2e})')

plt.xlabel('Количество чисел', fontsize=12)
plt.ylabel('Время выполнения (секунды)', fontsize=12)
plt.title('Сравнение алгоритмов проверки гипотезы Гольдбаха', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)

for i, (x, y) in enumerate(zip(test_sizes, execution_times_trivial)):
    plt.annotate(f'{y:.2f}с', (x, y), textcoords="offset points",
                 xytext=(0, 10), ha='center', fontsize=9, color='blue')

for i, (x, y) in enumerate(zip(test_sizes, execution_times_half)):
    plt.annotate(f'{y:.2f}с', (x, y), textcoords="offset points",
                 xytext=(0, -15), ha='center', fontsize=9, color='green')

plt.tight_layout()
plt.show()
