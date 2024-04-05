import tkinter as tk
import math
import fractions

last_calculations = []
memory_value = None
engineering_notation = False
last_result = None

def store_last_result(result):
    global last_result
    last_result = result

def clear():
    entry.delete(0, tk.END)


def insert_result(result):
    global last_calculations
    last_calculation = entry.get() + '=' + str(result)
    last_calculations.append(last_calculation)
    if len(last_calculations) > 3:
        last_calculations.pop(0)
    history_label.config(text='\n'.join(last_calculations))
    store_last_result(result)
    entry.delete(0, tk.END)
    entry.insert(tk.END, str(result))
    if result == int(result):
        result = int(result)
    else:
        result = float(result)
    clear()
    entry.insert(tk.END, str(result))

def evaluate_expression():
    try:
        expression = entry.get()
        expression = expression.replace('log', 'math.log10')
        expression = expression.replace('ln', 'math.log')
        expression = expression.replace('--', '+')
        expression = expression.replace('sqrt', 'math.sqrt')
        result = eval(expression)
        insert_result(result)
    except Exception as e:
        clear()
        entry.insert(tk.END, "Error")

def insert_character(char):
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
    entry.insert(tk.END, "**")

def insert_pow_2():
    current_text = entry.get()
    try:
        result = eval(f"{current_text} ** 2")
        insert_result(result)
    except Exception as e:
        clear()
        entry.insert(tk.END, "Error")

def insert_pow_3():
    current_text = entry.get()
    try:
        result = eval(f"{current_text} ** 3")
        insert_result(result)
    except Exception as e:
        clear()
        entry.insert(tk.END, "Error")

def insert_factorial():
    entry.insert(tk.END, "math.factorial(")

def delete_last_character():
    current_text = entry.get()
    if current_text:
        entry.delete(len(current_text) - 1, tk.END)

def calculate_percentage():
    try:
        expression = entry.get()
        if "+" in expression:
            value, percentage = expression.split("+")
            result = float(value) + (float(value) * (float(percentage) / 100))
        elif "-" in expression:
            value, percentage = expression.split("-")
            result = float(value) - (float(value) * (float(percentage) / 100))
        else:
            result = eval(expression)

        insert_result(result)
    except Exception as e:
        clear()
        entry.insert(tk.END, "Error")

def memory_add():
    global memory_value
    try:
        value = float(entry.get())
        memory_value = value
    except ValueError:
        pass

def memory_recall():
    global memory_value
    if memory_value is not None:
        entry.insert(tk.END, str(memory_value))

def update_display():
    current_text = entry.get()
    if engineering_notation:
        try:
            value = float(current_text)
            exponent = math.floor(math.log10(abs(value)))
            magnitude = value / (10 ** exponent)
            if magnitude == int(magnitude):
                entry.delete(0, tk.END)
                entry.insert(tk.END, f"{int(magnitude)}e{exponent}")
            else:
                entry.delete(0, tk.END)
                entry.insert(tk.END, f"{magnitude:.2f}e{exponent}")
        except ValueError:
            pass
    else:
        entry.delete(0, tk.END)
        entry.insert(tk.END, current_text)

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

def insert_negation():
    current_text = entry.get()
    if current_text.startswith('-'):
        entry.delete(0)
    else:
        entry.insert(0, "-")

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
        n = int(entry.get())
        clear()
        entry.insert(tk.END, str(n) + "C")
    except ValueError:
        clear()
        entry.insert(tk.END, "Error")

def n_choose_r():
    try:
        expression = entry.get()
        n, r = map(int, expression.split("C"))
        result = math.comb(n, r)
        clear()
        entry.insert(tk.END, str(result))
    except ValueError:
        clear()
        entry.insert(tk.END, "Error")

def polar_to_rectangular():
    try:
        expression = entry.get().strip()
        if expression:
            if ',' in expression:
                r, theta = map(float, expression.split(","))
            else:
                r = float(expression)
                theta = 0
            x = r * math.cos(math.radians(theta))
            y = r * math.sin(math.radians(theta))
            clear()
            entry.insert(tk.END, f"({x}, {y})")
        else:
            clear()
            entry.insert(tk.END, "Error: No input provided")
    except ValueError:
        clear()
        entry.insert(tk.END, "Error: Invalid input format")

def equals():
    if "C" in entry.get():
        n_choose_r()
    else:
        evaluate_expression()

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

history_label = tk.Label(window, fg="black", bg="#C5BD9E", text="", font=('Helvetica', 12), height=3, anchor='e', bd=5, relief='flat')
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
    ("RCL", memory_recall),
    ("M+", memory_add),
    ("x!", calculate_factorial),
    ("ab/c", absolute_value_or_fraction),
    ("Ans", lambda: insert_character(str(last_result))),
    ("nCr", combinations),
    ("Pol(", polar_to_rectangular),
    ("(-)", insert_negation),
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
    if text in ["sin", "cos", "tan", "π", "e", "log", "ln", "RCL", "M+", "x!", "ab/c", "Ans", "nCr", "Pol(", "(-)", "x²", "x³", "(", ")", "%"]:
        button = tk.Button(window, text=text, width=8, height=2, command=command, bg="black", fg="#FF5733",font=("Ariel",(12)))
    elif text in ["^","√","*","/","+","-"]:
        button = tk.Button(window, text=text, width=8, height=2, command=command, bg="grey", fg="black",font=("Ariel",(12)))
    elif text == "AC" or text == "=" or text == "DEL":
        button = tk.Button(window, text=text, width=8, height=2, command=command, bg="#FF5733", fg="black",font=("Ariel",(12)))
    else:
        button = tk.Button(window, text=text, width=8, height=2, command=command, bg="#B6BBC3", fg="black",font=("Ariel",(12)))
    button.grid(row=(i // 5) + 2, column=i % 5, padx=3, pady=5, sticky="nsew")


for i in range(2, len(buttons) // 5 + 3):
    window.grid_rowconfigure(i, weight=1)

for i in range(5):
    window.grid_columnconfigure(i, weight=1)

window.mainloop()