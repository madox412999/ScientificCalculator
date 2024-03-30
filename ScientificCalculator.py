import tkinter as tk
import math

last_result = None
memory_value = None
engineering_notation = False 

def clear():
    entry.delete(0, tk.END)

def evaluate_expression():
    global last_result
    try:
        result = eval(entry.get())
        last_result = result
        clear()
        entry.insert(tk.END, str(result))
    except Exception as e:
        clear()
        entry.insert(tk.END, "Error")

def insert_character(char):
    global last_result
    if char == "Ans" and last_result is not None:
        entry.insert(tk.END, str(last_result))
    else:
        entry.insert(tk.END, char)

def insert_pi():
    entry.insert(tk.END, str(math.pi))

def insert_e():
    entry.insert(tk.END, str(math.e))

def insert_sqrt():
    entry.insert(tk.END, "sqrt(")

def insert_pow():
    entry.insert(tk.END, "**")

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
        clear()
        entry.insert(tk.END, str(result))
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

def switch_to_eng_notation():
    global engineering_notation
    engineering_notation = not engineering_notation
    update_display()

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

window = tk.Tk()
window.title("Scientific Calculator")

entry = tk.Entry(window, font=('Helvetica', 20), justify='right')
entry.grid(row=0, column=0, columnspan=5, sticky="ew")

buttons = [
    ("sin", lambda: insert_character("sin(")),
    ("cos", lambda: insert_character("cos(")),
    ("tan", lambda: insert_character("tan(")),
    ("π", insert_pi),
    ("e", insert_e),
    ("√", insert_sqrt),
    ("^", insert_pow),
    ("(", lambda: insert_character("(")),
    (")", lambda: insert_character(")")),
    ("AC", clear),
    ("7", lambda: insert_character('7')),
    ("8", lambda: insert_character('8')),
    ("9", lambda: insert_character('9')),
    ("/", lambda: insert_character('/')),
    ("4", lambda: insert_character('4')),
    ("5", lambda: insert_character('5')),
    ("6", lambda: insert_character('6')),
    ("*", lambda: insert_character('*')),
    ("1", lambda: insert_character('1')),
    ("2", lambda: insert_character('2')),
    ("3", lambda: insert_character('3')),
    ("-", lambda: insert_character('-')),
    ("0", lambda: insert_character('0')),
    (".", lambda: insert_character('.')),
    ("+", lambda: insert_character('+')),
    ("=", evaluate_expression),
    ("Ans", lambda: insert_character('Ans')),
    ("DEL", delete_last_character),
    ("%", calculate_percentage),
    ("M+", memory_add),
    ("RCL", memory_recall),
    ("ENG", switch_to_eng_notation)
]

for i in range(8):
    window.grid_rowconfigure(i, weight=1)
for i in range(5):
    window.grid_columnconfigure(i, weight=1)

button_width = 10
button_height = 2

for i, (text, command) in enumerate(buttons):
    button = tk.Button(window, text=text, width=button_width, height=button_height, command=command)
    button.grid(row=(i // 5) + 1, column=i % 5, sticky="nsew")

window.mainloop()
