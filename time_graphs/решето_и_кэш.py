import time
import matplotlib.pyplot as plt
import numpy as np


def sieve_of_eratosthenes(max_n):
    is_prime = [True] * (max_n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, max_n + 1):
        if is_prime[i]:
            for j in range(i * i, max_n + 1, i):
                is_prime[j] = False
    return is_prime


def check_goldbach_sieve_cache_for_graph(max_N):
    start_time = time.time()

    is_prime = sieve_of_eratosthenes(max_N)

    prime_cache = {}

    def is_prime_cached(n):
        if n in prime_cache:
            return prime_cache[n]
        else:
            result = is_prime[n]
            prime_cache[n] = result
            return result

    for N in range(4, max_N + 1, 2):
        found = False

        for a in range(2, N):
            b = N - a

            if is_prime_cached(a) and is_prime_cached(b):
                found = True
                break

        if not found:
            return time.time() - start_time

    return time.time() - start_time


def check_goldbach_sieve_cache(max_N):
    is_prime = sieve_of_eratosthenes(max_N)

    prime_cache = {}
    cache_hits = 0
    cache_misses = 0

    def is_prime_cached(n):
        nonlocal cache_hits, cache_misses
        if n in prime_cache:
            cache_hits += 1
            return prime_cache[n]
        else:
            cache_misses += 1
            result = is_prime[n]
            prime_cache[n] = result
            return result

    for N in range(4, max_N + 1, 2):
        found = False

        for a in range(2, N):
            b = N - a

            if is_prime_cached(a) and is_prime_cached(b):
                found = True
                break

        if not found:
            return False

    return True


max_N = 50000
result = check_goldbach_sieve_cache(max_N)

test_sizes = [10000, 20000, 30000, 40000, 60000, 70000]
execution_times = []

for max_N in test_sizes:
    elapsed_time = check_goldbach_sieve_cache_for_graph(max_N)
    execution_times.append(elapsed_time)

n_array = np.array(test_sizes)
t_array = np.array(execution_times)

plt.figure(figsize=(10, 6))

plt.plot(test_sizes, execution_times, 'bo-', linewidth=2, markersize=8,
         label='Реальное время выполнения', markerfacecolor='blue')

k_values = t_array / (n_array ** 2)
k = np.mean(k_values)

n_smooth = np.linspace(min(test_sizes), max(test_sizes), 100)
t_theoretical = k * (n_smooth ** 2)

plt.plot(n_smooth, t_theoretical, 'r--', linewidth=2,
         label=f'Теоретическая O(n²)')

plt.xlabel('Количество чисел', fontsize=12)
plt.ylabel('Время выполнения (секунды)', fontsize=12)
plt.title('Проверка гипотезы Гольдбаха с оптимизацией - решето Эратосфена и кэширование', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)

for i, (x, y) in enumerate(zip(test_sizes, execution_times)):
    plt.annotate(f'{y:.2f}с', (x, y), textcoords="offset points",
                 xytext=(0, 10), ha='center', fontsize=9)

plt.tight_layout()
plt.show()
