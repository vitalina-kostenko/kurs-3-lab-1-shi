"""
Лабораторна робота №1. Завдання 1. Варіант 2.
Обчислення значень складної функції з урахуванням області визначення.

y = { 1 / (ctg(3-x) - arcsin(x)),       при x < 2
    { cos(1/(3-x)) / ln(2x-5),           при x > 2

Тригонометричні аргументи вводяться в градусах.
"""

import math
import tkinter as tk
from tkinter import messagebox


def deg_to_rad(degrees):
    return math.radians(degrees)


def ctg(x):
    """Котангенс: cos(x)/sin(x)"""
    sin_val = math.sin(x)
    if sin_val == 0:
        raise ValueError("Знаменник дорівнює нулю: sin(x) = 0 у котангенсі")
    return math.cos(x) / sin_val


def compute_y(x):
    """
    Обчислює значення складної функції для варіанту 2.
    Повертає (значення, опис_підфункції) або кидає виняток з причиною.
    """
    if x == 2:
        raise ValueError("Функція не визначена при x = 2 (x не належить жодній гілці)")

    if x < 2:
        subfunc = "y = 1 / (ctg(3 - x) - arcsin(x))"

        if abs(x) > 1:
            raise ValueError(f"arcsin(x) не визначений: |x| = {abs(x)} > 1")

        arg_ctg = 3 - x
        sin_arg = math.sin(arg_ctg)
        if abs(sin_arg) < 1e-15:
            raise ValueError(f"ctg(3 - x) не визначений: sin(3 - x) = 0 при x = {x}")

        ctg_val = ctg(arg_ctg)
        arcsin_val = math.asin(x)

        denominator = ctg_val - arcsin_val
        if abs(denominator) < 1e-15:
            raise ValueError(
                f"Знаменник дорівнює нулю: ctg(3 - x) - arcsin(x) = 0 при x = {x}"
            )

        y = 1.0 / denominator
        return y, subfunc

    else:  # x > 2
        subfunc = "y = cos(1/(3 - x)) / ln(2x - 5)"

        if x == 3:
            raise ValueError("Ділення на нуль: 3 - x = 0 при x = 3")

        ln_arg = 2 * x - 5
        if ln_arg <= 0:
            raise ValueError(
                f"ln(2x - 5) не визначений: 2x - 5 = {ln_arg} <= 0 при x = {x}"
            )
        if abs(ln_arg - 1) < 1e-15:
            raise ValueError(
                f"Знаменник дорівнює нулю: ln(2x - 5) = ln(1) = 0 при x = {x}"
            )

        cos_arg = 1.0 / (3 - x)
        cos_val = math.cos(cos_arg)
        ln_val = math.log(ln_arg)

        y = cos_val / ln_val
        return y, subfunc


def run_gui():
    """Запуск програми в окремому вікні (tkinter)."""

    def calculate():
        try:
            x_str = entry_x.get().strip()
            if not x_str:
                messagebox.showwarning("Увага", "Введіть значення x!")
                return

            x = float(x_str)

            is_degrees = var_degrees.get()
            if is_degrees:
                x_calc = deg_to_rad(x)
                input_info = f"x = {x}° ({x_calc:.6f} рад)"
            else:
                x_calc = x
                input_info = f"x = {x}"

            y, subfunc = compute_y(x_calc)
            result_text.set(
                f"Вхідні дані: {input_info}\n"
                f"Підфункція: {subfunc}\n"
                f"Результат: y = {y:.10f}"
            )

        except ValueError as e:
            result_text.set(f"Помилка: {e}")
        except Exception as e:
            result_text.set(f"Непередбачена помилка: {e}")

    root = tk.Tk()
    root.title("Завдання 1 — Варіант 2")
    root.geometry("550x300")
    root.resizable(False, False)

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Введіть значення x:").grid(row=0, column=0, sticky="w")
    entry_x = tk.Entry(frame, width=20)
    entry_x.grid(row=0, column=1, padx=5)

    var_degrees = tk.BooleanVar(value=False)
    tk.Checkbutton(
        frame,
        text="Аргумент у градусах (для триг. функцій)",
        variable=var_degrees,
    ).grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

    tk.Button(frame, text="Обчислити", command=calculate, width=15).grid(
        row=2, column=0, columnspan=2, pady=10
    )

    result_text = tk.StringVar(value="")
    tk.Label(
        frame,
        textvariable=result_text,
        justify=tk.LEFT,
        wraplength=500,
        font=("Consolas", 10),
    ).grid(row=3, column=0, columnspan=2, sticky="w")

    root.mainloop()


if __name__ == "__main__":
    run_gui()
