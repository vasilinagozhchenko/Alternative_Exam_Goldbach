import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def sieve_of_eratosthenes(max_n):
    if max_n < 2:
        return [False] * (max_n + 1)
    is_prime = [True] * (max_n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(max_n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, max_n + 1, i):
                is_prime[j] = False
    return is_prime


def check_goldbach_sequential(max_N, is_prime):
    for N in range(4, max_N + 1, 2):
        found = False
        for a in range(2, N // 2 + 1):
            b = N - a
            if is_prime[a] and is_prime[b]:
                found = True
                break
        if not found:
            raise RuntimeError(f"Контрпример найден: {N}")


def measure_time(max_N):
    start = time.perf_counter()
    is_prime = sieve_of_eratosthenes(max_N)
    check_goldbach_sequential(max_N, is_prime)
    end = time.perf_counter()
    return end - start


N_values = [5000000, 10000000, 15000000, 20000000, 25000000, 30000000, 35000000, 40000000, 45000000, 55000000]
times = []

for N in N_values:
    t = measure_time(N)
    times.append(t)
    print(f"N = {N}, время = {t:.2f} сек")

N_arr = np.array(N_values)
T_real = np.array(times)


def theoretical_func(x, k, c):
    return k * (x ** 2) + c


params, _ = curve_fit(theoretical_func, N_arr, T_real)
k_optimal, c_optimal = params

N_smooth = np.linspace(min(N_values), max(N_values), 500)
T_theory_smooth = theoretical_func(N_smooth, k_optimal, c_optimal)

plt.figure(figsize=(10, 6))
plt.plot(N_arr, T_real, 'o-', color='blue', linewidth=2, markersize=8,
         label='Реальное время выполнения')
plt.plot(N_smooth, T_theory_smooth, '--', color='red', linewidth=2,
         label=f'Теоретическое время O(n²/P) \nk = {k_optimal:.2e}')

plt.xlabel('Количество чисел ')
plt.ylabel('Время выполнения (секунды)')
plt.title('Провекра гипотезы Гольдбаха с комбинацией оптимизаций - многопоточность и Решето Эратосфена')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

for i, (x, y) in enumerate(zip(N_arr, T_real)):
    plt.annotate(f'{y:.2f}с', (x, y), textcoords="offset points",
                 xytext=(0, 10), ha='center', fontsize=9)

plt.tight_layout()
plt.show()
