import math
import tkinter as tk
from tkinter import messagebox


def deg_to_rad(degrees):
    return math.radians(degrees)


def ctg(x):
    sin_val = math.sin(x)
    if sin_val == 0:
        raise ValueError("Знаменник дорівнює нулю: sin(x) = 0 у котангенсі")
    return math.cos(x) / sin_val


def compute_y(x):
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
    else:
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
    key_value = [None]
    history = []

    def set_key():
        try:
            val = float(entry_key.get().strip())
            key_value[0] = val
            lbl_key_status.config(text=f"Ключове значення встановлено: {val}")
            entry_key.config(state="disabled")
            btn_set_key.config(state="disabled")
            entry_x.config(state="normal")
            btn_calc.config(state="normal")
        except ValueError:
            messagebox.showwarning("Увага", "Введіть коректне числове значення!")

    def calculate():
        if key_value[0] is None:
            messagebox.showwarning("Увага", "Спочатку задайте ключове значення!")
            return

        x_str = entry_x.get().strip()
        if not x_str:
            messagebox.showwarning("Увага", "Введіть значення x!")
            return

        try:
            x = float(x_str)
        except ValueError:
            messagebox.showwarning("Увага", "Некоректне числове значення x!")
            return

        if abs(x - key_value[0]) < 1e-12:
            messagebox.showinfo(
                "Завершення",
                f"Введено ключове значення x = {x}.\nПрограма завершує роботу.\n"
                f"Всього обчислень: {len(history)}",
            )
            root.destroy()
            return

        is_degrees = var_degrees.get()
        if is_degrees:
            x_calc = deg_to_rad(x)
            input_info = f"x = {x}° ({x_calc:.6f} рад)"
        else:
            x_calc = x
            input_info = f"x = {x}"

        try:
            y, subfunc = compute_y(x_calc)
            result = f"{input_info} → {subfunc} → y = {y:.10f}"
        except ValueError as e:
            result = f"{input_info} → Помилка: {e}"

        history.append(result)
        text_history.config(state="normal")
        text_history.insert(tk.END, f"{len(history)}. {result}\n")
        text_history.see(tk.END)
        text_history.config(state="disabled")
        entry_x.delete(0, tk.END)

    root = tk.Tk()
    root.title("Завдання 2 — Варіант 2 (цикл з ключовим значенням)")
    root.geometry("700x450")
    root.resizable(False, False)

    frame = tk.Frame(root, padx=15, pady=10)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Задайте ключове значення x:").grid(
        row=0, column=0, sticky="w"
    )
    entry_key = tk.Entry(frame, width=15)
    entry_key.grid(row=0, column=1, padx=5)
    btn_set_key = tk.Button(frame, text="Встановити", command=set_key)
    btn_set_key.grid(row=0, column=2, padx=5)
    lbl_key_status = tk.Label(frame, text="", fg="green")
    lbl_key_status.grid(row=0, column=3, sticky="w")

    tk.Label(frame, text="Введіть значення x:").grid(row=1, column=0, sticky="w", pady=(10, 0))
    entry_x = tk.Entry(frame, width=15, state="disabled")
    entry_x.grid(row=1, column=1, padx=5, pady=(10, 0))
    btn_calc = tk.Button(frame, text="Обчислити", command=calculate, state="disabled")
    btn_calc.grid(row=1, column=2, padx=5, pady=(10, 0))

    var_degrees = tk.BooleanVar(value=False)
    tk.Checkbutton(
        frame,
        text="Аргумент у градусах",
        variable=var_degrees,
    ).grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

    tk.Label(frame, text="Історія обчислень:").grid(
        row=3, column=0, columnspan=4, sticky="w"
    )
    text_history = tk.Text(frame, height=15, width=85, state="disabled", font=("Consolas", 9))
    text_history.grid(row=4, column=0, columnspan=4, pady=5)

    scrollbar = tk.Scrollbar(frame, command=text_history.yview)
    scrollbar.grid(row=4, column=4, sticky="ns")
    text_history.config(yscrollcommand=scrollbar.set)

    root.mainloop()


if __name__ == "__main__":
    run_gui()
