from cs50 import SQL
import hashlib
import getpass

db = SQL("sqlite:///atm.db")

def login():
    while True:
        print("Welcome to the ATM")
        print("1) Login")
        print("2) Register")
        print("3) Quit")
        choice = input("Choose an option: ")
        if choice == "1":
            user = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")
            if verify_user(user, password):
                return user
            else:
                print("Invalid username or password. Please try again.")
        elif choice == "2":
            register()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def verify_user(user, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    results = db.execute('SELECT * FROM info WHERE name = ? AND password = ?', user, hashed_password)
    return bool(results)

def register():
    user = input("Enter a new username: ")
    password = getpass.getpass("Enter a new password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    db.execute("INSERT INTO info (name, password, bal) VALUES (?, ?, 0)", user, hashed_password)
    print("Registration successful. You can now login.")

def main():
    while True:
        user = login()
        x = db.execute("SELECT * FROM info WHERE name = ?", user)
        if not x:
            print("Visit again.")
            return

        xx = x[0]
        balance = xx["bal"]

        while True:
            try:
                print(
                    """
                1) Balance
                2) Withdraw
                3) Deposit
                4) Logout
                    """
                )
                option = int(input("Enter Option: "))
            except ValueError:
                print("Please enter a number.")
                continue
            if option == 1:
                print("Balance:", balance)
            elif option == 2:
                withdraw = float(input("Enter the withdraw amount: "))
                if withdraw > balance:
                    print("Not enough balance.")
                else:
                    balance -= withdraw
                    print("Withdraw successful. New balance:", balance)
            elif option == 3:
                deposit = float(input("Enter the deposit amount: "))
                if deposit > 0:
                    balance += deposit
                    print("Deposit successful. New balance:", balance)
                else:
                    print("Invalid deposit amount.")
            elif option == 4:
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid option. Please choose again.")

            db.execute("UPDATE info SET bal = ? WHERE name = ?", balance, user)

if __name__ == "__main__":
    main()
