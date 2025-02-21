Password Manager

Description:
This is a simple password manager built with Python and Tkinter for securely storing and retrieving passwords. 
It includes features such as password generation, encryption, and retrieval using SQLite for storage and the cryptography library for encryption.

Features:
Generate Strong Passwords: Automatically generates a 12-character strong password.
Secure Storage: Encrypts and stores passwords securely in an SQLite database.
Retrieve Passwords: Allows retrieval of stored passwords by website name.
Clipboard Support: Copy passwords directly to the clipboard.
Password Visibility Toggle: Show or hide passwords as needed.

Prerequisites:
Ensure you have Python installed (version 3.6 or later).
Required Libraries

Install the required Python libraries using:
pip install cryptography

Usage:
Running the Application
Run the script using:
python password_manager.py

How It Works:
Generate a Password (Optional): Click "Generate Password" to create a random secure password.
Save a Password:
Enter the website, username, and password.
Click "Save Password" to encrypt and store it securely.
Retrieve a Password:
Enter the website name and click "Retrieve Password".
A popup will display the stored username and decrypted password.
Copy to Clipboard: Use the "Copy Password" button to copy retrieved passwords.
Toggle Password Visibility: Click the "Show" button to view the password, and "Hide" to mask it again.

File Structure:
password_manager.py   # Main script
passwords.db          # SQLite database (created automatically)
key.key               # Encryption key file (generated automatically)

Security Considerations:
The encryption key (key.key) is generated and stored locally. Keep it secure, as losing it means you cannot decrypt stored passwords.
The database (passwords.db) contains encrypted passwords but should still be stored securely.

License:
This project is open-source and free to use.
