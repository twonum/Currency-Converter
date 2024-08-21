import tkinter as tk
from tkinter import ttk, messagebox
import requests
from pygame import mixer
import speech_recognition as sr
import threading

# Initialize mixer for audio
mixer.init()

# Create the main window
root = tk.Tk()
root.title("Futuristic Currency Converter")
root.configure(bg="#1C1C1C")
root.geometry("920x500")

# Center the window on the screen
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"{width}x{height}+{x}+{y}")

# Load microphone image
microphone_image = tk.PhotoImage(file=r"images\microphone.png")

# Entry field for input
entryField = tk.Entry(root, font=('Roboto', 24, 'bold'), bg='#333333', fg='white', bd=5, relief=tk.RAISED, width=40)
entryField.grid(row=0, column=1, columnspan=6, padx=10, pady=10)

# Read-only text box for the result
resultField = tk.Text(root, font=('Roboto', 24, 'bold'), bg='#333333', fg='white', bd=5, relief=tk.RAISED, width=40, height=1)
resultField.grid(row=2, column=1, columnspan=6, padx=10, pady=10)
resultField.config(state=tk.DISABLED)

# Dropdown for "From" currency
from_currency = tk.StringVar()
from_currency_dropdown = ttk.Combobox(root, textvariable=from_currency, values=[], font=('Roboto', 16, 'bold'), width=20, state="readonly")
from_currency_dropdown.grid(row=1, column=1, padx=10, pady=10)
from_currency_dropdown.set("Select From Currency")

# Dropdown for "To" currency
to_currency = tk.StringVar()
to_currency_dropdown = ttk.Combobox(root, textvariable=to_currency, values=[], font=('Roboto', 16, 'bold'), width=20, state="readonly")
to_currency_dropdown.grid(row=1, column=2, padx=10, pady=10)
to_currency_dropdown.set("Select To Currency")

# Function to clear the entry field
def clear_entry():
    entryField.delete(0, tk.END)

# Offline exchange rates dictionary (expanded)
exchangeRates = {
    'USD': {'USD': 1, 'EUR': 0.85, 'JPY': 110.11, 'GBP': 0.75, 'AUD': 1.35, 'CAD': 1.32, 'CHF': 0.92, 'CNY': 6.45, 'INR': 74.12, 'NZD': 1.42},
    'EUR': {'USD': 1.18, 'EUR': 1, 'JPY': 129.41, 'GBP': 0.88, 'AUD': 1.57, 'CAD': 1.54, 'CHF': 1.08, 'CNY': 7.58, 'INR': 87.13, 'NZD': 1.67},
    'JPY': {'USD': 0.0091, 'EUR': 0.0077, 'JPY': 1, 'GBP': 0.0068, 'AUD': 0.012, 'CAD': 0.011, 'CHF': 0.0096, 'CNY': 0.067, 'INR': 0.68, 'NZD': 0.011},
    'GBP': {'USD': 1.34, 'EUR': 1.13, 'JPY': 146.94, 'GBP': 1, 'AUD': 1.79, 'CAD': 1.75, 'CHF': 1.22, 'CNY': 8.55, 'INR': 99.65, 'NZD': 1.93},
    'AUD': {'USD': 0.74, 'EUR': 0.64, 'JPY': 82.38, 'GBP': 0.56, 'AUD': 1, 'CAD': 0.98, 'CHF': 0.69, 'CNY': 4.84, 'INR': 54.96, 'NZD': 1.04},
    'CAD': {'USD': 0.76, 'EUR': 0.65, 'JPY': 83.78, 'GBP': 0.57, 'AUD': 1.02, 'CAD': 1, 'CHF': 0.7, 'CNY': 4.91, 'INR': 56.12, 'NZD': 1.06},
    'CHF': {'USD': 1.09, 'EUR': 0.92, 'JPY': 104.32, 'GBP': 0.82, 'AUD': 1.45, 'CAD': 1.43, 'CHF': 1, 'CNY': 7, 'INR': 80.43, 'NZD': 1.52},
    'CNY': {'USD': 0.15, 'EUR': 0.13, 'JPY': 14.95, 'GBP': 0.12, 'AUD': 0.21, 'CAD': 0.2, 'CHF': 0.14, 'CNY': 1, 'INR': 11.49, 'NZD': 0.22},
    'INR': {'USD': 0.013, 'EUR': 0.011, 'JPY': 1.47, 'GBP': 0.01, 'AUD': 0.018, 'CAD': 0.018, 'CHF': 0.012, 'CNY': 0.087, 'INR': 1, 'NZD': 0.019},
    'NZD': {'USD': 0.70, 'EUR': 0.60, 'JPY': 76.56, 'GBP': 0.52, 'AUD': 0.96, 'CAD': 0.94, 'CHF': 0.66, 'CNY': 4.50, 'INR': 52.27, 'NZD': 1},
}

# Variable to store the current mode (live or offline)
current_mode = "live"

# Function to fetch and display available currencies
def fetch_currencies():
    if current_mode == "live":
        url = "https://api.apilayer.com/fixer/symbols"
        headers = {"apikey": "YOUR KEU HERE!"}
        response = requests.get(url, headers=headers)
        data = response.json()
        currencies = list(data['symbols'].keys())
    else:
        currencies = list(exchangeRates.keys())
    
    from_currency_dropdown['values'] = currencies
    to_currency_dropdown['values'] = currencies

# Function to convert currency in live mode
def convert_currency_live():
    cfrom = from_currency.get()
    to = to_currency.get()
    amount = entryField.get()

    if not cfrom or not to or not amount:
        show_result("Please select currencies and enter amount")
        return

    try:
        amount = float(amount)
    except ValueError:
        show_result("Invalid amount")
        return

    url = f"https://api.apilayer.com/fixer/convert?to={to}&from={cfrom}&amount={amount}"
    headers = {"apikey": "YOUR KEU HERE!"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        show_result("Error in conversion")
    else:
        data = response.json()
        result = data['result']
        show_result(f'Converted Amount: {result:.2f} {to}')

# Function to convert currency in offline mode
def convert_currency_offline():
    cfrom = from_currency.get()
    to = to_currency.get()
    amount = entryField.get()

    if not cfrom or not to or not amount:
        show_result("Please select currencies and enter amount")
        return

    try:
        amount = float(amount)
    except ValueError:
        show_result("Invalid amount")
        return

    if cfrom in exchangeRates and to in exchangeRates[cfrom]:
        rate = exchangeRates[cfrom][to]
        result = amount * rate
        show_result(f'Converted Amount: {result:.2f} {to}')
    else:
        show_result("Conversion not possible")

# Function to convert currency based on the current mode
def convert_currency():
    if current_mode == "live":
        convert_currency_live()
    else:
        convert_currency_offline()

# Function to show results in the text box
def show_result(result):
    resultField.config(state=tk.NORMAL)
    resultField.delete(1.0, tk.END)
    resultField.insert(tk.END, result)
    resultField.config(state=tk.DISABLED)

# Function to switch between live and offline modes
def switch_mode():
    global current_mode
    if current_mode == "live":
        current_mode = "offline"
        mode_button.config(text="Switch to Live Mode")
        fetch_currencies()
    else:
        current_mode = "live"
        mode_button.config(text="Switch to Offline Mode")
        fetch_currencies()

# Voice recognition function
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = r.listen(source)
            text = r.recognize_google(audio)
            process_speech(text.lower())
        except sr.UnknownValueError:
            show_result("Could not understand the audio")
        except sr.RequestError:
            show_result("Service unavailable")

# Function to process speech input and perform conversion
def process_speech(text):
    words = text.split()
    amount = None
    for word in words:
        if word.isdigit() or (word.replace('.', '', 1).isdigit() and word.count('.') < 2):
            amount = word
            break

    if amount:
        entryField.delete(0, tk.END)
        entryField.insert(0, amount)
        
        for word in words:
            if word.upper() in exchangeRates.keys():
                if not from_currency.get():
                    from_currency.set(word.upper())
                else:
                    to_currency.set(word.upper())
                    break

        convert_currency()
    else:
        show_result("Unable to process the command")

# Function to start/stop listening for voice commands
def toggle_listen():
    if toggle_listen.is_listening:
        toggle_listen.is_listening = False
        show_result("Stopped Listening")
    else:
        toggle_listen.is_listening = True
        show_result("Listening...")
        threading.Thread(target=recognize_speech).start()

toggle_listen.is_listening = False

# Function to play a sound effect
def play_sound_effect():
    sound = mixer.Sound(r"C:\Users\DELL\OneDrive\Desktop\Self Study\Personal Projects\audio\music2.mp3")
    sound.play()

# Buttons
mode_button = tk.Button(root, text="Switch to Offline Mode", font=('Roboto', 16, 'bold'), bg='#555555', fg='white', bd=5, relief=tk.RAISED, command=switch_mode)
mode_button.grid(row=3, column=1, padx=10, pady=10)

clear_button = tk.Button(root, text="Clear", font=('Roboto', 16, 'bold'), bg='#555555', fg='white', bd=5, relief=tk.RAISED, command=clear_entry)
clear_button.grid(row=3, column=2, padx=10, pady=10)

convert_button = tk.Button(root, text="Convert", font=('Roboto', 16, 'bold'), bg='#555555', fg='white', bd=5, relief=tk.RAISED, command=lambda: [convert_currency(), play_sound_effect()])
convert_button.grid(row=3, column=3, padx=10, pady=10)

microphone_button = tk.Button(root, image=microphone_image, bd=5, relief=tk.RAISED, command=toggle_listen)
microphone_button.grid(row=3, column=4, padx=10, pady=10)

# Initialize currency data
fetch_currencies()

# Start the main loop
root.mainloop()
