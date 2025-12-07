import time
import matplotlib.pyplot as plt
import numpy as np


def sieve_of_eratosthenes(max_n):
    if max_n < 2:
        return [False] * (max_n + 1)
    is_prime = [True] * (max_n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(max_n**0.5) + 1):
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


N_values = [5000, 10000, 15000, 20000, 25000, 30000]
times = []

for N in N_values:
    t = measure_time(N)
    times.append(t)

N_arr = np.array(N_values)
T_real = np.array(times)

c = np.mean(T_real / (N_arr ** 2))
T_theory = c * N_arr ** 2

plt.figure(figsize=(10, 6))
plt.plot(N_arr, T_real, 'o-', color='blue', label='Реальное время выполнения')
plt.plot(N_arr, T_theory, '--', color='red', linewidth=2, label=r'Теоретическое время O(n²/P)')

plt.xlabel('Количество чисел')
plt.ylabel('Время выполнения (секунды)')
plt.title('Провекра гипотезы Гольдбаха с комбинацией оптимизаций - многопоточность и Решето Эратосфена')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

for i, (x, y) in enumerate(zip(N_arr, T_real)):
    plt.annotate(f'{y:.2f}с', (x, y), textcoords="offset points",
                 xytext=(0, 10), ha='center', fontsize=9)

plt.tight_layout()
plt.show()
