#Awrko's QuenchBot
import tkinter as tk
from tkinter import ttk

# Drink options and prices
drinks = {
    "Water" : 1.00,
    "RC Cola" : 1.50,
    "Green Tea" : 1.25,
    "Lemon Water" : 1.25,
    "Coffee Drink" : 1.50
}

# Virtual Coins
virtual_coins = [0.25, 0.50, 1.00, 2.00, 5.00]

# Window Initialization
window = tk.Tk()
window.title("Virtual Drink Vending Machine")
window.geometry("500x600")  # window size to 500x600 pixels

# Variables to track selections and payments
selected_drinks = []
total_price = 0.0
inserted_coins = 0.0

# Create a custom style for the different buttons
button_style = ttk.Style()
button_style.configure("Drink&Coin.TButton", font=("Arial", 10), width=20, foreground="black", background="green", padding=5)
button_style.configure("Payment.TButton", font=("Arial", 12), foreground="black", background="blue", padding=6)
button_style.configure("Stop.TButton", font=("Arial", 12), foreground="black", background="red", padding=6)
button_style.configure("Reset.TButton", font=("Arial", 12), foreground="black", background="orange", padding=6)
button_style.configure("Info.TLabel", font=("Arial", 10), foreground="black", padding=6)


# Function to handle drink selection
def select_drink(drink_name):
    global selected_drinks, total_price

    if drink_name in selected_drinks:
        selected_drinks.remove(drink_name)
        total_price -= drinks[drink_name]
    else:
        selected_drinks.append(drink_name)
        total_price += drinks[drink_name]

    update_total_display()

def reset_selections():
    global selected_drinks, total_price
    selected_drinks = []
    total_price = 0.0
    update_total_display()

# Function to update total price display
def update_total_display():
    total_label["text"] = f"Total: €{total_price:.2f}"

    # Enable the payment button if at least three drinks are selected
    if len(selected_drinks) >= 3:
        payment_button.config(state="normal")
        info_label.config(text="")
    else:
        payment_button.config(state="disabled")
        info_label.config(text="Select at least 3 drinks to activate payment")

# Function to handle coin insertion
def insert_coin(coin_value, balance_label):
    global inserted_coins, total_price
    inserted_coins += coin_value

    # Enable the "Payment" button if enough coins have been inserted
    if inserted_coins >= total_price:
        pay_button.config(state="normal")

    update_balance_display(balance_label)

# Function to update balance display
def update_balance_display(balance_label):
    balance = total_price - inserted_coins
    balance_label["text"] = f"Remaining amount: €{balance:.2f}"

def update_total_balance_display(total_balance_label):
    total_balance_label["text"] = f"Total Cost: €{total_price:.2f}"


# Function to handle the payment
def handle_payment():
    global selected_drinks, total_price, inserted_coins, pay_button
    window.withdraw()       #to the previous page

    # Create the payment window
    payment_window = tk.Toplevel(window)
    payment_window.title("Payment")
    payment_window.geometry("500x600")  #window size to 500x600 pixels

    # Frame to hold payment widgets
    payment_frame = ttk.Frame(payment_window)
    payment_frame.pack(padx=20, pady=20)

    # Payment Button (Initially disabled)
    pay_button = ttk.Button(payment_frame, text="Payment", state="disabled", style="Payment.TButton", command=lambda: process_payment(payment_window))
    pay_button.pack(pady=10)

    # STOP Button for the payment page
    stop_button = ttk.Button(payment_window, text="STOP", style="Stop.TButton", command=stop_program)
    stop_button.pack(pady=10)

    # Virtual Coins Buttons
    for coin_value in virtual_coins:
        coin_button = ttk.Button(payment_frame, text=f"€{coin_value:.2f}", style="Drink&Coin.TButton", command=lambda value=coin_value: insert_coin(value, balance_label))
        coin_button.pack(pady=5)

    # Total Balance Display
    total_balance_label = ttk.Label(payment_frame, text="Total Balance: $0.00", font=("Arial", 12))
    total_balance_label.pack(pady=(10, 0))

    # Balance Display (Renamed for clarity)
    balance_label = ttk.Label(payment_frame, text="Remaining Balance: €0.00", font=("Arial", 12))
    balance_label.pack(pady=(10, 0))

    # Update balance displays initially
    update_balance_display(balance_label)
    update_total_balance_display(total_balance_label)


# Function to process payment
def process_payment(payment_window):
    if inserted_coins >= total_price:
        payment_window.destroy()  # Closing payment window
        show_congratulations()

# Function to show congratulations / service page
def show_congratulations():
    congrats_window = tk.Toplevel(window)
    congrats_window.title("Congratulations!")
    congrats_window.geometry("500x500")  # Window size for service page

    message_label = ttk.Label(congrats_window, text="Enjoy your drink! Goodbye.", font=("Arial", 16))
    message_label.pack(pady=20)

    canvas = tk.Canvas(congrats_window, width=200, height=250)
    canvas.pack()

    #Animation glass size
    glass_outline = canvas.create_rectangle(50, 50, 150, 275, outline="blue")
    fill_level = canvas.create_rectangle(55, 275, 145, 275, fill="red")

    def animate_fill():
        nonlocal fill_level
        x1, y0, x2, y1 = canvas.coords(fill_level)
        if y0 > 60:  # Adjust based on glass height
            canvas.move(fill_level, 0, -5)  # Move the liquid up
            congrats_window.after(80, animate_fill)

    animate_fill()

    # STOP Button for the service page
    stop_button = ttk.Button(congrats_window, text="STOP", style="Stop.TButton", command=stop_program)
    stop_button.pack(pady=50)

# Function to stop the application
def stop_program():
    window.destroy()

# Drink Selection Buttons
for drink_name, price in drinks.items():
    button = ttk.Button(window, text=f"{drink_name} : €{price:.2f}", style="Drink&Coin.TButton", command=lambda name=drink_name: select_drink(name))
    button.pack(pady=5)

# Total Display
total_label = ttk.Label(window, text="Total: $0.00", font=("Arial", 12))
total_label.pack(pady=10)

# Info Label
info_label = ttk.Label(window, text="", style="Info.TLabel")
info_label.pack(pady=5)

# Payment Button
payment_button = ttk.Button(window, text="Payment", style="Payment.TButton", command=handle_payment, state="disabled")
payment_button.pack(pady=10)

# Reset Button
reset_button = ttk.Button(window, text="Reset", style="Reset.TButton", command=reset_selections)
reset_button.pack(pady=10)

# STOP Button
stop_button = ttk.Button(window, text="STOP", style="Stop.TButton", command=stop_program)
stop_button.pack(pady=10)

window.mainloop()
