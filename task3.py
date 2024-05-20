

import requests
import timeit

# Функція для завантаження тексту з URL
def download_text_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

# Визначаємо URL документів на Google Docs
url1 = 'https://docs.google.com/document/d/1pN3jIrmH_sUOyvAxvNfGH1Fc4fYD_pbcQAkjAYQkvqA/export?format=txt'
url2 = 'https://docs.google.com/document/d/1xP34L0bc0ERdyn_Zhk-54jJeqAjnNg_DX8B4NPNihkE/export?format=txt'

# Завантажуємо текстовий вміст з URL
text1 = download_text_from_url(url1)
text2 = download_text_from_url(url2)

# Визначаємо підрядки:
existing_pattern_text1 = "Двійковий або логарифмічний пошук часто використовується через швидкий час пошуку"  # Підрядок, який існує в text1
non_existing_pattern_text1 = "Бінарні діаграми рішень (BDD) – це економна форма представлення булевих функцій у вигляді орієнтованого ациклічного графу"  # Підрядок, якого немає в text1

existing_pattern_text2 = "Хеш-таблиця (hash map) – це структура даних, у якій пошук елементу здійснюється на основі його ключа"  # Підрядок, який існує в text2
non_existing_pattern_text2 = "направляємо індекс у middle+1, забираючи першу частину з переглянутого"  # Підрядок, якого немає в text2

# Алгоритм Боєра-Мура
def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1

# Алгоритм Кнута-Морріса-Пратта
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    M = len(pattern)
    N = len(text)
    lps = compute_lps(pattern)
    i = j = 0
    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == M:
            return i - j
        elif i < N and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

# Алгоритм Рабіна-Карпа
def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(text, pattern):
    substring_length = len(pattern)
    main_string_length = len(text)
    base = 256
    modulus = 101
    substring_hash = polynomial_hash(pattern, base, modulus)
    current_slice_hash = polynomial_hash(text[:substring_length], base, modulus)
    h_multiplier = pow(base, substring_length - 1) % modulus
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if text[i:i + substring_length] == pattern:
                return i
        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(text[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(text[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus
    return -1

# Вимірюємо час виконання за допомогою timeit
setup_code = """
from __main__ import boyer_moore_search, kmp_search, rabin_karp_search, text1, text2, existing_pattern_text1, non_existing_pattern_text1, existing_pattern_text2, non_existing_pattern_text2
"""

bm_existing_code1 = "boyer_moore_search(text1, existing_pattern_text1)"
bm_non_existing_code1 = "boyer_moore_search(text1, non_existing_pattern_text1)"
bm_existing_code2 = "boyer_moore_search(text2, existing_pattern_text2)"
bm_non_existing_code2 = "boyer_moore_search(text2, non_existing_pattern_text2)"

kmp_existing_code1 = "kmp_search(text1, existing_pattern_text1)"
kmp_non_existing_code1 = "kmp_search(text1, non_existing_pattern_text1)"
kmp_existing_code2 = "kmp_search(text2, existing_pattern_text2)"
kmp_non_existing_code2 = "kmp_search(text2, non_existing_pattern_text2)"

rk_existing_code1 = "rabin_karp_search(text1, existing_pattern_text1)"
rk_non_existing_code1 = "rabin_karp_search(text1, non_existing_pattern_text1)"
rk_existing_code2 = "rabin_karp_search(text2, existing_pattern_text2)"
rk_non_existing_code2 = "rabin_karp_search(text2, non_existing_pattern_text2)"

# Виконуємо timeit
bm_existing_time1 = timeit.timeit(setup=setup_code, stmt=bm_existing_code1, number=1000)
bm_non_existing_time1 = timeit.timeit(setup=setup_code, stmt=bm_non_existing_code1, number=1000)
bm_existing_time2 = timeit.timeit(setup=setup_code, stmt=bm_existing_code2, number=1000)
bm_non_existing_time2 = timeit.timeit(setup=setup_code, stmt=bm_non_existing_code2, number=1000)

kmp_existing_time1 = timeit.timeit(setup=setup_code, stmt=kmp_existing_code1, number=1000)
kmp_non_existing_time1 = timeit.timeit(setup=setup_code, stmt=kmp_non_existing_code1, number=1000)
kmp_existing_time2 = timeit.timeit(setup=setup_code, stmt=kmp_existing_code2, number=1000)
kmp_non_existing_time2 = timeit.timeit(setup=setup_code, stmt=kmp_non_existing_code2, number=1000)

rk_existing_time1 = timeit.timeit(setup=setup_code, stmt=rk_existing_code1, number=1000)
rk_non_existing_time1 = timeit.timeit(setup=setup_code, stmt=rk_non_existing_code1, number=1000)
rk_existing_time2 = timeit.timeit(setup=setup_code, stmt=rk_existing_code2, number=1000)
rk_non_existing_time2 = timeit.timeit(setup=setup_code, stmt=rk_non_existing_code2, number=1000)

# Виводимо результати
print(f"Boyer-Moore існуючий підрядок (text1): {bm_existing_time1}")
print(f"Boyer-Moore неіснуючий підрядок (text1): {bm_non_existing_time1}")
print(f"Boyer-Moore існуючий підрядок (text2): {bm_existing_time2}")
print(f"Boyer-Moore неіснуючий підрядок (text2): {bm_non_existing_time2}")

print(f"KMP існуючий підрядок (text1): {kmp_existing_time1}")
print(f"KMP неіснуючий підрядок (text1): {kmp_non_existing_time1}")
print(f"KMP існуючий підрядок (text2): {kmp_existing_time2}")
print(f"KMP неіснуючий підрядок (text2): {kmp_non_existing_time2}")

print(f"Rabin-Karp існуючий підрядок (text1): {rk_existing_time1}")
print(f"Rabin-Karp неіснуючий підрядок (text1): {rk_non_existing_time1}")
print(f"Rabin-Karp існуючий підрядок (text2): {rk_existing_time2}")
print(f"Rabin-Karp неіснуючий підрядок (text2): {rk_non_existing_time2}")
