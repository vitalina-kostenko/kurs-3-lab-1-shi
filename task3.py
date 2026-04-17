"""
Лабораторна робота №1. Завдання 3. Варіант 2.
Обчислення суми n елементів ряду:

S = cos(x-n-1)/sin(x) - sin(x-n-2)/cos(x^3) + cos(x-n-3)/sin(x^5) - ...

Три функції: for, while, рекурсія.
Кожна повертає (success: bool, result: float).
n ∈ N, x ∈ R.
"""

import math


def term(k, x, n):
    """
    Обчислює k-й член ряду (k від 1).
    Знак: (-1)^(k+1)
    Чисельник: cos(x-n-k) якщо k непарне, sin(x-n-k) якщо k парне
    Знаменник: sin(x^(2k-1)) якщо k непарне, cos(x^(2k-1)) якщо k парне
    """
    sign = (-1) ** (k + 1)

    arg_num = x - n - k
    if k % 2 == 1:
        numerator = math.cos(arg_num)
    else:
        numerator = math.sin(arg_num)

    power = 2 * k - 1
    x_pow = x ** power
    if k % 2 == 1:
        denominator = math.sin(x_pow)
    else:
        denominator = math.cos(x_pow)

    if abs(denominator) < 1e-15:
        raise ValueError(
            f"Знаменник дорівнює нулю у члені k={k}: "
            f"{'sin' if k % 2 == 1 else 'cos'}(x^{power}) = 0"
        )

    return sign * numerator / denominator


def sum_for(n, x):
    """Обчислення суми за допомогою циклу for."""
    try:
        s = 0.0
        for k in range(1, n + 1):
            s += term(k, x, n)
        return True, s
    except (ValueError, OverflowError, ZeroDivisionError) as e:
        return False, str(e)


def sum_while(n, x):
    """Обчислення суми за допомогою циклу while."""
    try:
        s = 0.0
        k = 1
        while k <= n:
            s += term(k, x, n)
            k += 1
        return True, s
    except (ValueError, OverflowError, ZeroDivisionError) as e:
        return False, str(e)


def sum_recursive(n, x, k=1, acc=0.0):
    """Обчислення суми за допомогою рекурсії."""
    try:
        if k > n:
            return True, acc
        acc += term(k, x, n)
        return sum_recursive(n, x, k + 1, acc)
    except (ValueError, OverflowError, ZeroDivisionError) as e:
        return False, str(e)


def main():
    print("=" * 60)
    print("Завдання 3 — Варіант 2")
    print("Обчислення суми ряду:")
    print("S = cos(x-n-1)/sin(x) - sin(x-n-2)/cos(x³)")
    print("    + cos(x-n-3)/sin(x⁵) - ...")
    print("=" * 60)

    while True:
        try:
            n = int(input("\nВведіть n (натуральне число): "))
            if n <= 0:
                print("n повинно бути натуральним числом (> 0)!")
                continue
            break
        except ValueError:
            print("Некоректне значення! Введіть ціле число.")

    while True:
        try:
            x = float(input("Введіть x (дійсне число): "))
            break
        except ValueError:
            print("Некоректне значення! Введіть число.")

    print(f"\nВхідні дані: n = {n}, x = {x}")
    print("-" * 60)

    success_for, result_for = sum_for(n, x)
    if success_for:
        print(f"Цикл FOR:    S = {result_for:.10f}")
    else:
        print(f"Цикл FOR:    Помилка — {result_for}")

    success_while, result_while = sum_while(n, x)
    if success_while:
        print(f"Цикл WHILE:  S = {result_while:.10f}")
    else:
        print(f"Цикл WHILE:  Помилка — {result_while}")

    success_rec, result_rec = sum_recursive(n, x)
    if success_rec:
        print(f"Рекурсія:    S = {result_rec:.10f}")
    else:
        print(f"Рекурсія:    Помилка — {result_rec}")

    if success_for and success_while and success_rec:
        print("-" * 60)
        print("Усі три методи дали однаковий результат:", end=" ")
        if abs(result_for - result_while) < 1e-12 and abs(result_for - result_rec) < 1e-12:
            print("ТАК")
        else:
            print("НІ (можливі похибки округлення)")

    print()


if __name__ == "__main__":
    main()
