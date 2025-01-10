import random
import re
import sqlite3

# Establish the database connection
conn = sqlite3.connect('banking_system.db')
cursor = conn.cursor()

# Create Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    account_number INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    dob TEXT NOT NULL,
    password TEXT NOT NULL,
    balance REAL NOT NULL,
    contact TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    address TEXT NOT NULL,
    active BOOLEAN NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number INTEGER NOT NULL,
    type TEXT NOT NULL,
    amount REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_number) REFERENCES users(account_number)
)
""")
conn.commit()

# Add User
def add_user():
    print("\n-------- Add New User --------")
    name = input("Enter your name: ")
    city = input("Enter your city: ")
    dob = input("Enter your date of birth (dd/mm/yyyy): ")

    password = input("Enter your password: ")
    while len(password) < 6 or not password.isalnum():
        print("Password must be at least 6 characters and alphanumeric.")
        password = input("Enter your password: ")

    initial_balance = float(input("Enter your initial balance: "))
    while initial_balance < 2000:
        print("Initial balance must be at least 2000.")
        initial_balance = float(input("Enter your initial balance: "))

    contact = input("Enter your contact number: ")
    while not contact.isdigit() or len(contact) != 10:
        print("Invalid contact number. Please enter a 10-digit number.")
        contact = input("Enter your contact number: ")

    email = input("Enter your email address: ")
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    while not re.match(pattern, email):
        print("Invalid email address.")
        email = input("Enter your email address: ")

    address = input("Enter your address: ")
    account_number = random.randint(1000000000, 9999999999)

    try:
        cursor.execute("""
        INSERT INTO users (account_number, name, city, dob, password, balance, contact, email, address, active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (account_number, name, city, dob, password, initial_balance, contact, email, address, True))
        conn.commit()
        print("User added successfully!")
        print("Account Number:", account_number)
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")

# Show User
def show_user():
    print("\n-------- Show User --------")
    account_number = int(input("Enter your account number: "))
    cursor.execute("SELECT * FROM users WHERE account_number = ?", (account_number,))
    user = cursor.fetchone()
    if user:
        print("\n-------- User Information --------")
        print(f"Account Number: {user[0]}")
        print(f"Name: {user[1]}")
        print(f"City: {user[2]}")
        print(f"DOB: {user[3]}")
        print(f"Balance: {user[5]}")
        print(f"Contact: {user[6]}")
        print(f"Email: {user[7]}")
        print(f"Address: {user[8]}")
        print(f"Active: {'Yes' if user[9] else 'No'}")
    else:
        print("User not found.")

# Login
def login():
    print("\n-------- Login --------")
    account_number = int(input("Enter your account number: "))
    password = input("Enter your password: ")
    cursor.execute("SELECT * FROM users WHERE account_number = ? AND password = ?", (account_number, password))
    user = cursor.fetchone()
    if user:
        print("Login successful!")
        return account_number
    else:
        print("Invalid account number or password.")
        return None

# Account Menu
def login_menu(account_number):
    while True:
        print("\n-------- Account Menu --------")
        print("1. Show Balance")
        print("2. Show Transactions")
        print("3. Credit Amount")
        print("4. Debit Amount")
        print("5. Logout")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            cursor.execute("SELECT balance FROM users WHERE account_number = ?", (account_number,))
            balance = cursor.fetchone()[0]
            print(f"Your current balance is {balance}")

        elif choice == 2:
            cursor.execute("SELECT * FROM transactions WHERE account_number = ?", (account_number,))
            transactions = cursor.fetchall()
            if transactions:
                for txn in transactions:
                    print(f"{txn[3]}: {txn[2]} {txn[1]} - {txn[4]}")
            else:
                print("No transactions found.")

        elif choice == 3:
            amount = float(input("Enter the amount to credit: "))
            cursor.execute("UPDATE users SET balance = balance + ? WHERE account_number = ?", (amount, account_number))
            cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (?, 'Credit', ?)", (account_number, amount))
            conn.commit()
            print("Amount credited successfully.")

        elif choice == 4:
            amount = float(input("Enter the amount to debit: "))
            cursor.execute("SELECT balance FROM users WHERE account_number = ?", (account_number,))
            balance = cursor.fetchone()[0]
            if amount <= balance:
                cursor.execute("UPDATE users SET balance = balance - ? WHERE account_number = ?", (amount, account_number))
                cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (?, 'Debit', ?)", (account_number, amount))
                conn.commit()
                print("Amount debited successfully.")
            else:
                print("Insufficient balance.")

        elif choice == 5:
            print("Logging out...")
            break

        else:
            print("Invalid choice.")

# Main Menu
def main():
    while True:
        print("\n-------- Main Menu --------")
        print("1. Add User")
        print("2. Show User")
        print("3. Login")
        print("4. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            add_user()
        elif choice == 2:
            show_user()
        elif choice == 3:
            account_number = login()
            if account_number:
                login_menu(account_number)
        elif choice == 4:
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice.")

# Run the program
main()

# Close the database connection
conn.close()

#end code