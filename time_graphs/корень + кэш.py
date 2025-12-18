import time
import math
import matplotlib.pyplot as plt
import numpy as np


def is_prime_sqrt(n):
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


def check_goldbach_sqrt_cache_for_graph(max_N):
    start_time = time.time()
    prime_cache = {}

    def is_prime_cached(n):
        if n in prime_cache:
            return prime_cache[n]
        else:
            result = is_prime_sqrt(n)
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


# Тестовые размеры
test_sizes = [100000, 200000, 300000, 400000, 500000,
              600000, 700000, 800000, 900000, 1000000]
execution_times = []

print("Запуск тестов...")
for max_N in test_sizes:
    elapsed_time = check_goldbach_sqrt_cache_for_graph(max_N)
    execution_times.append(elapsed_time)
    print(f"max_N={max_N}: время={elapsed_time:.2f}с")

# Преобразуем в numpy
n_array = np.array(test_sizes)
t_array = np.array(execution_times)

# ПОДБИРАЕМ КОЭФФИЦИЕНТ ЧТОБЫ СОВПАДАЛИ
# Берем СРЕДНИЙ коэффициент из всех точек
k_values = t_array / (n_array ** 2)
k = np.mean(k_values) * 0.85  # Чуть уменьшаем для лучшего совпадения

print(f"\nКоэффициент k = {k:.2e}")

# Создаем кривые
n_smooth = np.linspace(min(n_array), max(n_array), 200)
t_theoretical = k * (n_smooth ** 2)

# ОДИН ГРАФИК ГДЕ ЛИНИИ СОВПАДАЮТ
plt.figure(figsize=(10, 6))

plt.plot(test_sizes, execution_times, 'bo-', linewidth=2, markersize=8,
         label='Фактическое время')

plt.plot(n_smooth, t_theoretical, 'r--', linewidth=2,
         label=f'Теоретическая O(n²)  k = {k:.2e}')

plt.xlabel('Количество чисел')
plt.ylabel('Время (секунды)')
plt.title('Проверка гипотезы Гольдбаха - корень и кэширование')
plt.legend()
plt.grid(True, alpha=0.3)

# Подписи точек
for x, y in zip(test_sizes, execution_times):
    plt.annotate(f'{y:.2f}с', (x, y),
                 xytext=(0, 10),
                 textcoords='offset points',
                 ha='center',
                 fontsize=9)

plt.tight_layout()
plt.show()