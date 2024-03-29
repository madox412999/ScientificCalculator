import tkinter as tk
import math

def clear():
    entry.delete(0, tk.END)

def evaluate_expression():
    try:
        result = eval(entry.get())
        clear()
        entry.insert(tk.END, str(result))
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
    entry.insert(tk.END, "sqrt(")

def insert_pow():
    entry.insert(tk.END, "**")

def insert_factorial():
    entry.insert(tk.END, "math.factorial(")

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
    ("C", clear),
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
    ("=", evaluate_expression)
]

for i, (text, command) in enumerate(buttons):
    button = tk.Button(window, text=text, width=5, height=2, command=command)
    button.grid(row=(i // 5) + 1, column=i % 5, padx=5, pady=5)

window.mainloop()
