import tkinter as tk
import math
import fractions

last_calculations = []
last_result = None


def clear():
    entry.delete(0, tk.END)


def insert_result(result):
    global last_calculations
    current_text = entry.get()
    last_calculation = current_text + '=' + str(result)
    last_calculations.append(last_calculation)
    if len(last_calculations) > 3:
        last_calculations.pop(0)
    history_label.config(text='\n'.join(last_calculations))

    if isinstance(result, float):
        if result.is_integer():
            result = int(result)
        else:
            result = str(result).rstrip('0').rstrip('.')
    clear()
    entry.insert(tk.END, str(result))


def evaluate_expression():
    try:
        expression = entry.get()
        expression = expression.replace('log', 'math.log10')
        expression = expression.replace('ln', 'math.log')
        expression = expression.replace('--', '+')
        expression = expression.replace('sqrt', 'math.sqrt')
        expression = expression.replace('^', '**')
        # Handle trigonometric functions separately
        trig_functions = ['sin', 'cos', 'tan']
        for func in trig_functions:
            expression = expression.replace(func, f'math.{func}')

        result = eval(expression)
        insert_result(result)
    except Exception as e:
        print(f"{e}")
        clear()
        entry.insert(tk.END, "Error")


def insert_character(char):
    current_text = entry.get()
    if current_text == "Error":
        clear()
    if char == "0" or (current_text and current_text[-1].isdigit() and char.isdigit()):
        entry.insert(tk.END, char)
    elif char in ["sin(", "cos(", "tan("]:
        entry.delete(0, tk.END)
        entry.insert(tk.END, char + current_text + ")")
    else:
        entry.insert(tk.END, char)


def insert_pi():
    entry.insert(tk.END, str(math.pi))


def insert_e():
    entry.insert(tk.END, str(math.e))


def insert_sqrt():
    current_text = entry.get()
    if current_text.strip():
        entry.delete(0, tk.END)
        entry.insert(tk.END, f"sqrt({current_text})")
    else:
        entry.insert(tk.END, "sqrt(")


def insert_pow():
    entry.insert(tk.END, "^")


def insert_pow_2():
    current_text = entry.get()
    try:
        result = eval(f"{current_text} ** 2")
        insert_result(result)
        history_label_text = f"{current_text}^2={result}"
        last_calculations.append(history_label_text)
        if len(last_calculations) > 3:
            last_calculations.pop(0)
        history_label.config(text='\n'.join(last_calculations))
    except Exception as e:
        print(f"{e}")
        clear()
        entry.insert(tk.END, "Error")


def insert_pow_3():
    current_text = entry.get()
    try:
        result = eval(f"{current_text} ** 3")
        insert_result(result)
        history_label_text = f"{current_text}^3={result}"
        last_calculations.append(history_label_text)
        if len(last_calculations) > 3:
            last_calculations.pop(0)
        history_label.config(text='\n'.join(last_calculations))
    except Exception as e:
        print(f"{e}")
        clear()
        entry.insert(tk.END, "Error")


def insert_factorial():
    entry.insert(tk.END, "math.factorial(")


def delete_last_character():
    current_text = entry.get()
    if current_text:
        entry.delete(len(current_text) - 1, tk.END)


def calculate_percentage():
    result = None
    history_label_text = None
    try:
        expression = entry.get()
        if expression.strip() == "":
            raise ValueError("No expression to calculate percentage")

        if any(op in expression for op in ["+", "-", "*", "/"]):
            if "+" in expression:
                value, percentage = expression.split("+")
                result = float(value) + (float(value) * (float(percentage) / 100))
                history_label_text = f"{value}+{percentage}%={result}"
            elif "-" in expression:
                value, percentage = expression.split("-")
                result = float(value) - (float(value) * (float(percentage) / 100))
                history_label_text = f"{value}-{percentage}%={result}"
            elif "*" in expression:
                value, percentage = expression.split("*")
                result = float(value) * (1 + float(percentage) / 100)
                history_label_text = f"{value}*{percentage}%={result}"
            elif "/" in expression:
                value, percentage = expression.split("/")
                result = float(value) / (1 - float(percentage) / 100)
                history_label_text = f"{value}/{percentage}%={result}"
        else:
            raise ValueError("Invalid expression for percentage calculation")

        clear()
        entry.insert(tk.END, str(result))
        last_calculations.append(history_label_text)
        if len(last_calculations) > 3:
            last_calculations.pop(0)
        history_label.config(text='\n'.join(last_calculations))
    except Exception as e:
        print(f"{e}")
        clear()
        entry.insert(tk.END, "Error")


def insert_log():
    current_text = entry.get()
    if current_text.strip():
        entry.delete(0, tk.END)
        entry.insert(tk.END, f"log({current_text})")
    else:
        entry.insert(tk.END, "log(")


def insert_ln():
    current_text = entry.get()
    if current_text.strip():
        entry.delete(0, tk.END)
        entry.insert(tk.END, f"ln({current_text})")
    else:
        entry.insert(tk.END, "ln(")


def absolute_value_or_fraction():
    current_text = entry.get().strip()
    try:
        value = float(current_text)
        if value < 0:
            result = abs(value)
        else:
            if value.is_integer():
                result = int(value)
            else:
                fraction = fractions.Fraction(value).limit_denominator()
                result = f"{fraction.numerator}/{fraction.denominator}"
    except ValueError:
        result = "Error"

    clear()
    entry.insert(tk.END, str(result))


def combinations():
    try:
        expression = entry.get().replace(" ", "")
        if "nCr" in expression:
            n, r = map(int, expression.split("nCr"))
            result = math.comb(n, r)
            clear()
            entry.insert(tk.END, str(result))
        else:
            entry.insert(tk.END, "nCr")
    except ValueError:
        clear()
        entry.insert(tk.END, "Error")


def equals():
    try:
        expression = entry.get()
        if "nCr" in expression:
            combinations()
        else:
            evaluate_expression()
    except Exception as e:
        print(f"Exception occurred: {e}")
        clear()
        entry.insert(tk.END, "Error")


def calculate_factorial():
    try:
        n = int(entry.get())
        result = math.factorial(n)
        insert_result(result)
    except ValueError:
        clear()
        entry.insert(tk.END, "Error")


window = tk.Tk()
window.title("Scientific Calculator")

history_label = tk.Label(window, fg="black", bg="#C5BD9E", text="", font=('Helvetica', 12), height=3, anchor='e', bd=5,
                         relief='flat')
history_label.grid(row=0, column=0, columnspan=5, sticky="ew")

entry = tk.Entry(window, font=('Helvetica', 20), justify='right', bg="#AFE7EB", bd=5, relief='ridge')
entry.grid(row=1, column=0, columnspan=5, sticky="ew")

buttons = [
    ("sin", lambda: insert_character("sin(")),
    ("cos", lambda: insert_character("cos(")),
    ("tan", lambda: insert_character("tan(")),
    ("π", insert_pi),
    ("e", insert_e),
    ("log", insert_log),
    ("ln", insert_ln),
    ("x!", calculate_factorial),
    ("ab/c", absolute_value_or_fraction),
    ("nCr", combinations),
    ("x²", insert_pow_2),
    ("x³", insert_pow_3),
    ("(", lambda: insert_character("(")),
    (")", lambda: insert_character(")")),
    ("%", calculate_percentage),
    ("7", lambda: insert_character('7')),
    ("8", lambda: insert_character('8')),
    ("9", lambda: insert_character('9')),
    ("√", insert_sqrt),
    ("^", insert_pow),
    ("4", lambda: insert_character('4')),
    ("5", lambda: insert_character('5')),
    ("6", lambda: insert_character('6')),
    ("*", lambda: insert_character('*')),
    ("/", lambda: insert_character('/')),
    ("1", lambda: insert_character('1')),
    ("2", lambda: insert_character('2')),
    ("3", lambda: insert_character('3')),
    ("+", lambda: insert_character('+')),
    ("-", lambda: insert_character('-')),
    ("0", lambda: insert_character('0')),
    (".", lambda: insert_character('.')),
    ("DEL", delete_last_character),
    ("AC", clear),
    ("=", equals),
]

for i, (text, command) in enumerate(buttons):
    if text in ["sin", "cos", "tan", "π", "e", "log", "ln", "x!", "ab/c", "nCr", "x²", "x³", "(", ")", "%"]:
        button = tk.Button(window, text=text, width=8, height=2, command=command, bg="black", fg="#FF5733",
                           font=("Ariel", 12))
    elif text in ["^", "√", "*", "/", "+", "-"]:
        button = tk.Button(window, text=text, width=8, height=2, command=command, bg="grey", fg="black",
                           font=("Ariel", 12))
    elif text == "AC" or text == "=" or text == "DEL":
        button = tk.Button(window, text=text, width=8, height=2, command=command, bg="#FF5733", fg="black",
                           font=("Ariel", 12))
    else:
        button = tk.Button(window, text=text, width=8, height=2, command=command, bg="#B6BBC3", fg="black",
                           font=("Ariel", 12))
    button.grid(row=(i // 5) + 2, column=i % 5, padx=3, pady=5, sticky="nsew")

for i in range(2, len(buttons) // 5 + 3):
    window.grid_rowconfigure(i, weight=1)

for i in range(5):
    window.grid_columnconfigure(i, weight=1)

window.mainloop()
