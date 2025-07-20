import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import string
import pyperclip

class PasswordNameDialog(tk.simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Enter the name for this password:").grid(row=0)
        self.result = tk.Entry(master)
        self.result.grid(row=0, column=1)
        return self.result

    def apply(self):
        self.result_name = self.result.get()

# Counter to keep track of appended passwords
password_counter = 1

def generate_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError("Length must be a positive integer.")
        
        uppercase = uppercase_var.get()
        lowercase = lowercase_var.get()
        special_chars = special_chars_var.get()

        if not (uppercase or lowercase or special_chars):
            messagebox.showerror("Error", "Please select at least one option.")
            return

        characters = ''
        if uppercase:
            characters += string.ascii_uppercase
        if lowercase:
            characters += string.ascii_lowercase
        if special_chars:
            characters += string.punctuation

        password = ''.join(random.choice(characters) for _ in range(length))
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

        # Evaluate password strength
        strength = "Weak" if length < 8 else "Medium" if length < 12 else "Strong"
        strength_label.config(text=f"Password Strength: {strength}")
    
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid integer for the password length.")

def handle_save_exception(password, name):
    global password_counter
    
    with open("generated_passwords.txt", "a") as file:
        if name:
            file.write(f"{name}: {password}\n")
        else:
            global password_counter
            file.write(f"password{password_counter}: {password}\n")
            password_counter += 1
    messagebox.showinfo("Success", "Password saved successfully.")
    
def save_password():
    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "No password generated yet.")
        return

    dialog = PasswordNameDialog(window)
    try:
        if dialog.result_name:
            handle_save_exception(password, dialog.result_name)
        else:
            handle_save_exception(password, None)
    except AttributeError as e:
        messagebox.showerror("Error", "Failed to save password")

# Function to copy password to clipboard
def copy_password():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Success", "Password copied to clipboard.")
    else:
        messagebox.showerror("Error", "No password generated yet.")

# Create tkinter window
window = tk.Tk()
window.title("Password Generator")
window.config(bg="lightyellow3")

# Create widgets
length_label = tk.Label(window, text="Password Length:", fg='#5E2612', bg='salmon')
length_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
length_entry = tk.Entry(window)
length_entry.grid(row=0, column=1, padx=10, pady=5)

uppercase_var = tk.BooleanVar()
uppercase_check = tk.Checkbutton(window, text="Include Uppercase Letters", variable=uppercase_var, bg='#FBECDE', fg='brown')
uppercase_check.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

lowercase_var = tk.BooleanVar()
lowercase_check = tk.Checkbutton(window, text="Include Lowercase Letters", variable=lowercase_var, bg='#FBECDE', fg='brown')
lowercase_check.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

special_chars_var = tk.BooleanVar()
special_chars_check = tk.Checkbutton(window, text="Include Special Characters", variable=special_chars_var, bg='#FBECDE', fg='brown')
special_chars_check.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

generate_button = tk.Button(window, text="Generate Password", command=generate_password, fg='blue', bg='white')
generate_button.grid(row=4, column=0, columnspan=5, padx=10, pady=20)

password_label = tk.Label(window, text="Generated Password:", fg='#5E2612', bg='salmon')
password_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
password_entry = tk.Entry(window)
password_entry.grid(row=5, column=1, padx=10, pady=5)

strength_label = tk.Label(window, text="Password Strength:", fg='brown', bg='#FEBAAD')
strength_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

save_button = tk.Button(window, text="Save Password", command=save_password, fg="blue", bg='palegreen1')
save_button.grid(row=7, column=0, columnspan=5, padx=10, pady=5)

copy_button = tk.Button(window, text="Copy to Clipboard", command=copy_password, fg="blue", bg='palegreen1')
copy_button.grid(row=8, column=0, columnspan=5, padx=10, pady=5)

# Run the tkinter event loop
window.mainloop()
