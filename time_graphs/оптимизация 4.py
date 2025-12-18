import time
import matplotlib.pyplot as plt
import numpy as np

prime_cache = {}


def is_prime_cached(n):
    if n in prime_cache:
        return prime_cache[n]

    result = is_prime_naive(n)
    prime_cache[n] = result
    return result


def is_prime_naive(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def check_goldbach_cached(max_N):
    start_time = time.time()

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


test_sizes = [10000, 20000, 30000, 40000, 50000]
execution_times = []

for max_N in test_sizes:
    prime_cache.clear()  

    elapsed_time = check_goldbach_cached(max_N)
    execution_times.append(elapsed_time)
    print(f"max_N={max_N}: {elapsed_time:.2f} сек")

n_array = np.array(test_sizes)
t_array = np.array(execution_times)

coeffs = np.polyfit(n_array, t_array, 2)

log_n = np.log(n_array)
log_t = np.log(t_array)
coeff_log = np.polyfit(log_n, log_t, 1)

k_values = t_array / (n_array ** 2)

k_median = np.median(k_values)

q25, q75 = np.percentile(k_values, [25, 75])
iqr = q75 - q25
lower_bound = q25 - 1.5 * iqr
upper_bound = q75 + 1.5 * iqr

filtered_k = k_values[(k_values >= lower_bound) & (k_values <= upper_bound)]
k_filtered_mean = np.mean(filtered_k) if len(filtered_k) > 0 else np.mean(k_values)
k = k_filtered_mean

plt.figure(figsize=(12, 8))

plt.plot(test_sizes, execution_times, 'bo-', linewidth=2, markersize=8,
         label='Реальное время выполнения', markerfacecolor='blue', markeredgecolor='black')

n_smooth = np.linspace(min(test_sizes), max(test_sizes), 500)
t_theoretical_quadratic = k * (n_smooth ** 2)
plt.plot(n_smooth, t_theoretical_quadratic, 'r--', linewidth=2,
         label=f'Квадратичная O(n²) \n k = {k:.2e}')


plt.xlabel('Максимальное число N', fontsize=12)
plt.ylabel('Время выполнения (секунды)', fontsize=12)
plt.title('Проверка гипотезы Гольдбаха - кэшированиие', fontsize=14)
plt.legend(fontsize=10, loc='upper left')
plt.grid(True, alpha=0.3)
plt.yscale('linear')  

for i, (x, y) in enumerate(zip(test_sizes, execution_times)):
    plt.annotate(f'{y:.1f}с', (x, y), textcoords="offset points",
                 xytext=(0, 10), ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.show()
