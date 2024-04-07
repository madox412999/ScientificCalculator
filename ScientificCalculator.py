import tkinter as tk
import math
import fractions

last_calculations = []  # list for history label


def clear():
    entry.delete(0, tk.END)


def insert_result(result):
    global last_calculations
    current_text = entry.get()
    last_calculation = current_text + '=' + str(result)  # Create a string representing the calculation result
    last_calculations.append(last_calculation)  # Append the calculation result to the list of last calculations
    if len(last_calculations) > 3:  # Check if the number of calculations stored is greater than 3
        last_calculations.pop(0)  # If so, remove the oldest calculation from the list
        # Update the text displayed in the history label by joining the calculations with newline characters
    history_label.config(text='\n'.join(last_calculations))

    if isinstance(result, float):  # Check if the result is a float
        # If the result is a float,convert it to a string and remove  trailing zeros and decimal point
        result = str(result).rstrip('0').rstrip('.')
    clear()
    entry.insert(tk.END, str(result))


def evaluate_expression():
    try:
        expression = entry.get()  # Get the expression from the entry widget
        expression = expression.replace('log', 'math.log10')  # Replace 'log' with 'math.log10'
        expression = expression.replace('ln', 'math.log')  # Replace 'ln' with 'math.log'
        expression = expression.replace('--', '+')  # Replace '--' with '+'
        expression = expression.replace('sqrt', 'math.sqrt')  # Replace 'sqrt' with 'math.sqrt'
        expression = expression.replace('^', '**')  # Replace '^' with '**'
        # Handle trigonometric functions separately
        trig_functions = ['sin', 'cos', 'tan']
        for func in trig_functions:
            # Replace trigonometric functions with their math module equivalents
            expression = expression.replace(func, f'math.{func}')

        result = eval(expression)  # Evaluate the expression
        insert_result(result)  # Insert the result into the entry widget
    except Exception as e:
        print(f"{e}")  # Print the exception message to the console
        clear()  # Clear the entry widget
        entry.insert(tk.END, "Error")  # Insert "Error" into the entry widget


def insert_character(char):
    current_text = entry.get()
    if current_text == "Error":
        clear()
    # Check if the character is a digit or if it's a valid continuation of the current expression
    if char == "0" or (current_text and current_text[-1].isdigit() and char.isdigit()):
        entry.insert(tk.END, char)
    # If the character is a trigonometric function, add it to the current expression with parentheses
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
    if current_text.strip():  # Check if there is any non-whitespace text in the entry
        entry.delete(0, tk.END)  # If there is non-whitespace text, delete it and insert "sqrt(current_text)"
        entry.insert(tk.END, f"sqrt({current_text})")
    else:
        entry.insert(tk.END, "sqrt(")  # If there is no text, insert "sqrt("


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


def delete_last_character():
    current_text = entry.get()
    if current_text:
        entry.delete(len(current_text) - 1, tk.END)


def calculate_percentage():
    result = None
    history_label_text = None
    try:
        expression = entry.get()
        if expression.strip() == "":  # Check if the expression is empty
            raise ValueError("No expression to calculate percentage")

        # Check if the expression contains any arithmetic operators
        if any(op in expression for op in ["+", "-", "*", "/"]):
            # Perform percentage calculation based on the operator
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

        clear()  # Clear the entry widget
        entry.insert(tk.END, str(result))  # inserting the result
        last_calculations.append(history_label_text)  # Update the history label
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
    current_text = entry.get().strip()  # Get the current text in the entry field and remove leading,trailing whitespace
    try:
        value = float(current_text)  # Attempt to convert the current text to a float
        if value < 0:  # Check if the value is negative
            result = abs(value)  # If negative, calculate the absolute value
        else:  # If positive or zero, check if the value is an integer
            if value.is_integer():  # If integer, convert to int(get the number without decimal part,for example 5.0=5)
                result = int(value)
            else:  # If not an integer, convert to a fraction
                fraction = fractions.Fraction(value).limit_denominator()
                result = f"{fraction.numerator}/{fraction.denominator}"
    except ValueError:
        result = "Error"

    clear()
    entry.insert(tk.END, str(result))


def combinations():
    try:
        # Get the expression from the entry widget and remove spaces
        expression = entry.get().replace(" ", "")
        if "nCr" in expression:  # Check if the expression contains "nCr"
            # If yes, split the expression around "nCr" and convert the parts to integers
            n, r = map(int, expression.split("nCr"))
            # Calculate the combination (n choose r) using math.comb
            result = math.comb(n, r)
            # Clear the entry widget and insert the result
            clear()
            entry.insert(tk.END, str(result))
        else:
            entry.insert(tk.END, "nCr")  # If "nCr" is not in the expression, insert "nCr" into the entry widget
    except ValueError:
        clear()
        entry.insert(tk.END, "Error")


def equals():
    try:
        expression = entry.get()
        if "nCr" in expression:  # Check if the expression involves combinations
            combinations()  # If so, calculate combinations
        else:
            evaluate_expression()  # Otherwise, evaluate the expression
    except Exception as e:
        print(f"Exception occurred: {e}")
        clear()
        entry.insert(tk.END, "Error")


def calculate_factorial():
    try:
        n = int(entry.get())  # Get the integer value from the entry widget
        result = math.factorial(n)  # Calculate the factorial of the value
        insert_result(result)  # Insert the result into the entry widget
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
# Iterate through the list of buttons and their associated commands
for i, (text, command) in enumerate(buttons):
    # Determine the appearance of the button based on its text
    if text in ["sin", "cos", "tan", "π", "e", "log", "ln", "x!", "ab/c", "nCr", "x²", "x³", "(", ")", "%"]:
        button = tk.Button(window, text=text, width=8, height=2, command=command, bg="black", fg="#FF5733",
                           font=("Ariel", 12))
    elif text in ["^", "√", "*", "/", "+", "-"]:
        button = tk.Button(window, text=text, width=8, height=2, command=command, bg="grey", fg="black",
                           font=("Ariel", 12))
    elif text in ["AC", "=", "DEL"]:
        button = tk.Button(window, text=text, width=8, height=2, command=command, bg="#FF5733", fg="black",
                           font=("Ariel", 12))
    else:
        button = tk.Button(window, text=text, width=8, height=2, command=command, bg="#B6BBC3", fg="black",
                           font=("Ariel", 12))
    button.grid(row=(i // 5) + 2, column=i % 5, padx=3, pady=5, sticky="nsew")
# Configure row weights to ensure proper resizing
for i in range(2, len(buttons) // 5 + 3):
    window.grid_rowconfigure(i, weight=1)

# Configure column weights to ensure proper resizing
for i in range(5):
    window.grid_columnconfigure(i, weight=1)

window.mainloop()
