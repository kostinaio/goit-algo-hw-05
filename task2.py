

def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (high + low) // 2

        # якщо x більше за значення посередині списку, ігноруємо ліву половину
        if arr[mid] < x:
            low = mid + 1

        # якщо x менше за значення посередині списку, ігноруємо праву половину
        elif arr[mid] > x:
            high = mid - 1
            upper_bound = arr[mid] if upper_bound is None else min(upper_bound, arr[mid])

        # інакше x присутній на позиції і повертаємо кортеж
        else:
            upper_bound = arr[mid]
            return (iterations, upper_bound)

    # якщо елемент не знайдений, верхня межа буде arr[low] якщо low в межах масиву
    if upper_bound is None and low < len(arr):
        upper_bound = arr[low]
    elif upper_bound is None:
        upper_bound = None

    return (iterations, upper_bound)

# Тестуємо функцію
arr = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7]
x = 4.4
result = binary_search(arr, x)
print(f"Element {x} found in {result[0]} iterations with upper bound {result[1]}")

x = 4.5
result = binary_search(arr, x)
print(f"Element {x} found in {result[0]} iterations with upper bound {result[1]}")

x = 8.0
result = binary_search(arr, x)
print(f"Element {x} found in {result[0]} iterations with upper bound {result[1]}")
