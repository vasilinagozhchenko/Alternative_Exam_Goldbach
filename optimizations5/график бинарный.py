import time
import math
import matplotlib.pyplot as plt
import numpy as np
import bisect


def find_goldbach_numbers(max_N):
    start_time = time.perf_counter()
    is_prime = [True] * (max_N + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(math.sqrt(max_N)) + 1):
        if is_prime[i]:
            for j in range(i * i, max_N + 1, i):
                is_prime[j] = False

    primes = [i for i in range(2, max_N + 1) if is_prime[i]]
    can_be_goldbach = [False] * (max_N + 1)

    for i, a in enumerate(primes):
        max_b = max_N - a

        j_max = bisect.bisect_right(primes, max_b) - 1

        if j_max >= i:
            for j in range(i, j_max + 1):
                b = primes[j]
                s = a + b
                if s % 2 == 0:
                    can_be_goldbach[s] = True

    for N in range(4, max_N + 1, 2):
        if not can_be_goldbach[N]:
            break

    end_time = time.perf_counter()
    return end_time - start_time


N_values = [10000, 30000, 50000, 150000, 250000, 300000, 400000, 450000, 500000]
times = []

for N in N_values:
    t = find_goldbach_numbers(N)
    times.append(t)
    print(f"N = {N:7d}: {t:.3f} секунд")

N_arr = np.array(N_values)
T_real = np.array(times)

logN = np.log(N_arr)
denominator = (N_arr ** 2) / (logN ** 2)
T_norm = T_real / denominator

c = np.mean(T_norm)
T_theory = c * denominator

plt.figure(figsize=(10, 6))
plt.plot(N_arr, T_real, 'o-', color='blue', label='Реальное время выполнения', linewidth=2)
plt.plot(N_arr, T_theory, '--', color='red', linewidth=2, label=fr'Теоретическое O(n²/(ln(n))²) k={c:.2e}')
plt.xlabel('Количество чисел')
plt.ylabel('Время выполнения (секунды)')
plt.title('Проверка гипотезы Гольдбаха с бинарным поиском')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

for i, (x, y) in enumerate(zip(N_arr, T_real)):
    plt.annotate(f'{y:.2f}с', (x, y), textcoords="offset points",
                 xytext=(0, 10), ha='center', fontsize=9)

plt.tight_layout()
plt.show()