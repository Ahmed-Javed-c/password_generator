import tkinter as tk
from tkinter import messagebox
import random
import string
import sqlite3
from cryptography.fernet import Fernet

# Generate and save encryption key
KEY_FILE = "key.key"
def load_key():
    try:
        with open(KEY_FILE, "rb") as file:
            return file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as file:
            file.write(key)
        return key

key = load_key()
cipher = Fernet(key)

# Database setup
conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS passwords (website TEXT, username TEXT, password TEXT)")
conn.commit()

# Function to generate strong passwords
def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(12))
    
    # Make password visible when generated
    entry_password.config(show="")  
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)

# Function to toggle password visibility
def toggle_password():
    if entry_password.cget("show") == "":
        entry_password.config(show="*")  # Hide password
        btn_toggle_password.config(text="Show")
    else:
        entry_password.config(show="")   # Show password
        btn_toggle_password.config(text="Hide")

# Function to copy text to clipboard
def copy_to_clipboard(text):
    app.clipboard_clear()
    app.clipboard_append(text)
    app.update()  # Keeps clipboard data available after app closes
    messagebox.showinfo("Copied", "Password copied to clipboard!")

# Function to save password
def save_password():
    website = entry_website.get()
    username = entry_username.get()
    password = entry_password.get()
    
    if not website or not username or not password:
        messagebox.showwarning("Warning", "All fields must be filled!")
        return
    
    encrypted_password = cipher.encrypt(password.encode()).decode()
    cursor.execute("INSERT INTO passwords VALUES (?, ?, ?)", (website, username, encrypted_password))
    conn.commit()
    messagebox.showinfo("Success", "Password saved successfully!")
    entry_website.delete(0, tk.END)
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)

# Function to retrieve password
def retrieve_password():
    website = entry_website.get()
    cursor.execute("SELECT username, password FROM passwords WHERE website = ?", (website,))
    result = cursor.fetchone()
    
    if result:
        username, encrypted_password = result
        decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
        
        # Create a popup with the password and a copy button
        popup = tk.Toplevel(app)
        popup.title("Password Retrieved")
        popup.geometry("300x150")

        tk.Label(popup, text=f"Username: {username}").pack(pady=5)
        tk.Label(popup, text=f"Password: {decrypted_password}").pack(pady=5)

        tk.Button(popup, text="Copy Password", command=lambda: copy_to_clipboard(decrypted_password)).pack(pady=5)

    else:
        messagebox.showerror("Error", "No password found for this website!")

# GUI Setup
app = tk.Tk()
app.title("Password Manager")
app.geometry("300x200")



tk.Label(app, text="Website:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_website = tk.Entry(app)
entry_website.grid(row=3, column=1, padx=10, pady=5)

# Username
tk.Label(app, text="Username:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_username = tk.Entry(app)
entry_username.grid(row=2, column=1, padx=10, pady=5)

# Password
tk.Label(app, text="Password:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_password = tk.Entry(app, show="*")
entry_password.grid(row=0, column=1, padx=10, pady=5)

# Buttons
tk.Button(app, text="Generate Password",  command=generate_password).grid(row=1, column=1, columnspan=2, pady=0)
btn_toggle_password = tk.Button(app, text="Show", fg="#FFFFFF", bg="#000000", command=toggle_password)
btn_toggle_password.grid(row=0, column=2, columnspan=2, pady=5)
tk.Button(app, text="Save Password" , command=save_password).grid(row=6, column=1, columnspan=2, pady=0)
tk.Button(app, text="Retrieve Password" , command=retrieve_password).grid(row=7, column=1, columnspan=2, pady=5)
tk.Button(app, text="Exit" , fg="#FFFFFF", bg="#000000", command=app.quit).grid(row=7, column=2, columnspan=2, pady=5)

app.mainloop()

# Close database connection
conn.close()
