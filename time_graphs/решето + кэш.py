import time
import matplotlib.pyplot as plt
import numpy as np
import math


def sieve_of_eratosthenes(max_n):
    if max_n < 2:
        return [False, False]

    is_prime = [True] * (max_n + 1)
    is_prime[0] = is_prime[1] = False

    limit = int(math.sqrt(max_n)) + 1
    for i in range(2, limit):
        if is_prime[i]:
            for j in range(i * i, max_n + 1, i):
                is_prime[j] = False
    return is_prime


def check_goldbach_sieve_with_real_cache(max_N):
    start_time = time.time()
    is_prime_array = sieve_of_eratosthenes(max_N)
    pair_cache = {}

    for N in range(4, max_N + 1, 2):
        found = False

        for a in range(2, N):
            b = N - a
            cache_key = (a, b)

            if cache_key in pair_cache:
                if pair_cache[cache_key]:
                    found = True
                    break
                continue

            a_is_prime = is_prime_array[a]
            b_is_prime = is_prime_array[b]

            result = a_is_prime and b_is_prime
            pair_cache[cache_key] = result

            if result:
                found = True
                break

        if not found:
            return time.time() - start_time

    return time.time() - start_time


test_sizes = [1000000, 2000000, 3000000, 4000000, 5000000]
execution_times = []

for max_N in test_sizes:
    elapsed_time = check_goldbach_sieve_with_real_cache(max_N)
    execution_times.append(elapsed_time)
    print(f"N={max_N}, время={elapsed_time:.2f}с")

n_array = np.array(test_sizes)
t_array = np.array(execution_times)

k_values = t_array / (n_array ** 2)
k = np.mean(k_values)

n_smooth = np.linspace(min(test_sizes), max(test_sizes), 100)
t_theoretical = k * (n_smooth ** 2)

plt.figure(figsize=(10, 6))

plt.plot(test_sizes, execution_times, 'bo-', linewidth=2, markersize=8,
         label=f'Экспериментальное время')

plt.plot(n_smooth, t_theoretical, 'r--', linewidth=2,
         label=f'Теоретическая O(n²)\nk = {k:.2e}')

plt.xlabel('Количество чисел (N)', fontsize=12)
plt.ylabel('Время выполнения (секунды)', fontsize=12)
plt.title('Проверка гипотезы Гольдбаха - кэширование и решето', fontsize=14)
plt.legend(fontsize=12, loc='upper left')
plt.grid(True, alpha=0.3)

for x, y in zip(test_sizes, execution_times):
    plt.annotate(f'{y:.2f}с', (x, y), textcoords="offset points",
                 xytext=(0, 10), ha='center', fontsize=9)

plt.tight_layout()
plt.show()
