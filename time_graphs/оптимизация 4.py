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
    """Версия без вывода для измерения времени"""
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


# Сначала соберем данные
test_sizes = [10000, 20000, 30000, 40000, 50000]
execution_times = []

print("Измерение времени выполнения...")
for max_N in test_sizes:
    prime_cache.clear()  # Очищаем кэш для каждого теста

    elapsed_time = check_goldbach_cached(max_N)
    execution_times.append(elapsed_time)
    print(f"max_N={max_N}: {elapsed_time:.2f} сек")

# Преобразуем в массивы numpy
n_array = np.array(test_sizes)
t_array = np.array(execution_times)

# ВАЖНО: Проверим данные на аномалии
print("\nАнализ данных:")
print("N\tВремя\tN²\tВремя/N²")
for n, t in zip(test_sizes, execution_times):
    print(f"{n}\t{t:.2f}\t{n ** 2:.2e}\t{t / (n ** 2):.2e}")

# ПРАВИЛЬНОЕ ВЫЧИСЛЕНИЕ КОЭФФИЦИЕНТА
# Для O(n²): t = k * n²
# Используем линейную регрессию через полиномиальную аппроксимацию

# Способ 1: Используем полиномиальную регрессию 2-й степени
coeffs = np.polyfit(n_array, t_array, 2)
print(f"\nКоэффициенты полинома 2-й степени: a={coeffs[0]:.2e}, b={coeffs[1]:.2e}, c={coeffs[2]:.2e}")
# Для больших n основной вклад дает a*n²

# Способ 2: Линейная регрессия log(t) от log(n)
log_n = np.log(n_array)
log_t = np.log(t_array)
coeff_log = np.polyfit(log_n, log_t, 1)
print(f"\nЛогарифмическая регрессия: log(t) = {coeff_log[0]:.4f}*log(n) + {coeff_log[1]:.4f}")
print(f"Степень роста: {coeff_log[0]:.4f} (ожидается ~2 для O(n²))")

# Способ 3: Взвешенное среднее (исключая аномальные значения)
# Вычислим k_i = t_i / n_i² для каждого измерения
k_values = t_array / (n_array ** 2)
print(f"\nОтдельные значения k = t/N²:")
for i, k in enumerate(k_values):
    print(f"  N={test_sizes[i]}: k={k:.2e}")

# Исключим явные выбросы (например, очень большие или маленькие значения)
# Берем медиану для устойчивости к выбросам
k_median = np.median(k_values)
print(f"\nМедиана k: {k_median:.2e}")

# Берем среднее без экстремальных значений
q25, q75 = np.percentile(k_values, [25, 75])
iqr = q75 - q25
lower_bound = q25 - 1.5 * iqr
upper_bound = q75 + 1.5 * iqr

filtered_k = k_values[(k_values >= lower_bound) & (k_values <= upper_bound)]
k_filtered_mean = np.mean(filtered_k) if len(filtered_k) > 0 else np.mean(k_values)
print(f"Среднее k (без выбросов): {k_filtered_mean:.2e}")

# Используем среднее значение k для графика
k = k_filtered_mean
print(f"\nИспользуемый коэффициент k = {k:.2e}")

# Построение графика
plt.figure(figsize=(12, 8))

# Реальные данные
plt.plot(test_sizes, execution_times, 'bo-', linewidth=2, markersize=8,
         label='Реальное время выполнения', markerfacecolor='blue', markeredgecolor='black')

# Теоретическая кривая O(n²) с вычисленным коэффициентом
n_smooth = np.linspace(min(test_sizes), max(test_sizes), 500)
t_theoretical_quadratic = k * (n_smooth ** 2)
plt.plot(n_smooth, t_theoretical_quadratic, 'r--', linewidth=2,
         label=f'Квадратичная O(n²) \n k = {k:.2e}')


plt.xlabel('Максимальное число N', fontsize=12)
plt.ylabel('Время выполнения (секунды)', fontsize=12)
plt.title('Проверка гипотезы Гольдбаха - кэшированиие', fontsize=14)
plt.legend(fontsize=10, loc='upper left')
plt.grid(True, alpha=0.3)
plt.yscale('linear')  # Можно попробовать 'log' если данные очень разбросаны

# Добавляем подписи значений
for i, (x, y) in enumerate(zip(test_sizes, execution_times)):
    plt.annotate(f'{y:.1f}с', (x, y), textcoords="offset points",
                 xytext=(0, 10), ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()


plt.show()