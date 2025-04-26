import pandas as pd
import csv
import sqlite3
import sys
import pwinput
import datetime
import matplotlib.pyplot as plt


con = sqlite3.connect('bank_sim.db')

cur = con.cursor()


"""
Prompts user for username and password and verifies it within the database.
Continues prompting until correct credentials are entered and proceeds to main menu after.

Returns:
    str username: Returns the usename of the logged in user 
"""
def login_check():
    print("Welcome to Mini Bank Menu")
    while True:
        username = input("Username: ")
        password = pwinput.pwinput(prompt='Password: ')

        find_username = cur.execute("SELECT username FROM customers WHERE username = ?", (username,)).fetchone()
        if find_username:
            find_password = cur.execute("SELECT * FROM customers WHERE username = ? AND password = ?", (username, password)).fetchone()
            if find_password:
                print("successful login")
                return username
            else:
                print("Access denied")





"""
Description:
Displays the main menu for the user to enable access the rest of the program.

Parameters:

Menu options:
- customer/admin login (customer information)
- accounts menu (info with options: deposit, withdraw)
- loans menu (view loans with options: new loan, payoff loan, check )

"""
def main_menu(username):
    if username == "adminuser":
        while True:
            print("\nAdmin Menu:")
            print("a. Stats menu")
            print("b. Graph information")
            print("c. Logout")

            choice = input("Enter your choice (a,b,c, or d): ")

            if choice == 'a':
                print("You selected Option 1")
                admin_stats_menu(username)
            elif choice == 'b':
                print("You selected Option 2")
                admin_graph_menu(username)
            elif choice == 'c':
                print("Exiting...")
                con.close()
                sys.exit()
            else:
                print("Invalid input. Please enter a,b,c, or d: ")
    else:
        while True:
            print("\nCustomer Menu:")
            print("a. Customer Information")
            print("b. Account(s) information")
            print("c. Outstanding loans")
            print("d. Logout")

            choice = input("Enter your choice (a,b,c, or d): ")

            if choice == 'a':
                print("You selected Option 1")
                customer_cust_menu(username)
            elif choice == 'b':
                print("You selected Option 2")
                customer_accounts_menu(username)
            elif choice == 'c':
                print("You selected Option 3")
                customer_loan_menu(username)
            elif choice == 'd':
                print("Exiting...")
                con.close()
                sys.exit()
            else:
                print("Invalid input. Please enter a,b,c, or d: ")


def admin_stats_menu(admin_user):

    cur.execute("""
                SELECT c.first_name, c.last_name, a.balance
                FROM accounts a
                JOIN customers c ON a.customer_id = c.customer_id
                WHERE a.balance = (SELECT MIN(balance) FROM accounts);
                """)
    result = cur.fetchone()
    if result:
        first_name, last_name, balance = result
        print("\n\nCustomer with the lowest balance:")
        print(f"First Name: {first_name} Last Name: {last_name} Balance: {balance}")
    else:
        print("Error fetching data")

    cur.execute("""
                SELECT c.first_name, c.last_name, a.balance
                FROM accounts a
                JOIN customers c ON a.customer_id = c.customer_id
                WHERE a.balance = (SELECT MAX(balance) FROM accounts);
                """)
    result = cur.fetchone()
    if result:
        first_name, last_name, balance = result
        print("\nCustomer with the Highest balance:")
        print(f"First Name: {first_name}, Last Name: {last_name}, Balance: {balance}")
    else:
        print("Error fetching data")

    cur.execute("SELECT AVG(balance) AS mean_amount FROM accounts;")
    result = cur.fetchone()
    print(f"\nAverage Balance: {result[0]:,.2f}")


    while True:
        print("\nChoose an option:")
        print("a. Go back")

        choice = input("Enter your choice (a): ")

        if choice == 'a':
            main_menu(admin_user)

def admin_graph_menu (admin_user):
    while True:
        print("\nGraph Options:")
        print("1. Bar chart of total balance per customer")
        print("2. Pie chart of loan distribution by type")
        print("3. Go back")

        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            cur.execute("""
                SELECT c.first_name || ' ' || c.last_name AS name, SUM(a.balance)
                FROM accounts a
                JOIN customers c ON a.customer_id = c.customer_id
                GROUP BY c.customer_id
            """)

            data = cur.fetchall()
            if data:
                names = [row[0] for row in data]
                balances = [row[1] for row in data]
                plt.figure(figsize=(12, 5))
                plt.bar(names, balances, color='skyblue')
                plt.title("Total Balance per Customer")
                plt.xticks(rotation=45, ha='right')
                plt.ylabel("Balance ($)")
                plt.tight_layout()
                plt.show()
            else:
                print("Error")

        elif choice == '2':
            cur.execute("SELECT loan_type, COUNT(*) FROM loans GROUP BY loan_type")

            data = cur.fetchall()
            if data:
                types = [row[0] for row in data]
                counts = [row[1] for row in data]

                plt.figure(figsize=(6, 6))
                plt.pie(counts, labels=types, autopct='%1.1f%%')
                plt.title("Loan Type Distribution")
                plt.axis('equal')
                plt.tight_layout()
                plt.show()
            else:
                print("Error")

        elif choice == '3':
            main_menu(admin_user)
        else:
            print("Invalid input. Please choose 1, 2, or 3")



def customer_cust_menu(cust_user):
    print("\n\nCustomer Information:")
    cur.execute("SELECT first_name, last_name, email, phone_number, address, date_of_birth FROM customers WHERE username = ?;", (cust_user,))
    result = cur.fetchone()
    if result:
        first_name, last_name, email, phone_number, address, date_of_birth = result
        print(f"First Name: {first_name} \nLast Name: {last_name} \nEmail: {email} \nPhone #: {phone_number} \nDOB: {date_of_birth} \nAddress :{address}")
    else:
        print("Error fetching data")


    while True:
        print("\nChoose an option:")
        print("a. Go back")
        print("b. Edit Info")

        choice = input("Enter your choice (a or b): ")

        if choice == 'a':
            main_menu(cust_user)
        elif choice == 'b':
            print("\nAvailable Columns: \nemail \npassword \nfirst_name \nlast_name \ndate_of_birth")
            column_to_edit = input("Which column would you like to edit? ")
            change_to_column = input(f"What would you like to change {column_to_edit} to? ")

            columnsData = cur.execute("PRAGMA table_info(customers)").fetchall()
            column_names = [col[1] for col in columnsData]
            if column_to_edit in column_names:
                    query = f"UPDATE customers SET {column_to_edit} = ? WHERE username = ?"
                    cur.execute(query, (change_to_column, cust_user))
                    con.commit()

        else:
            print("Invalid input. Please choose a or b")

def customer_accounts_menu (cust_user):
    print("\n\nAccounts :")
    cust_id = cur.execute("SELECT customer_id FROM customers WHERE username = ?;", (cust_user,)).fetchone()[0]
    cur.execute("SELECT account_id, account_type, balance, opened_on FROM accounts WHERE customer_id = ? ORDER BY balance DESC;", (cust_id,))

    results = cur.fetchall()
    if results:
        for row in results:
            print(f"Account ID: {row[0]} Account Type: {row[1]}, Current Balance: {row[2]}, Created on: {row[3]}")
    else:
        print("Error fetching data")


    while True:
        print("\nChoose an option:")
        print("a. Go back")
        print("b. Account options")

        choice = input("Enter your choice (a or b): ")

        if choice == 'a':
            main_menu(cust_user)
        elif choice == 'b':
            while True:
                print("\nAccount Options:")
                print("a. Deposit into an account")
                print("b. Withdraw from an account")
                print("c. Add or Delete an account")

                account_choice = input("Enter your choice (a, b, or c): ")

                if account_choice == 'a':

                    account_to_deposit = input("Which Account ID would you like to deposit into? : ")
                    deposit_amount = input("How much would you like to deposit? : ")
                    cur.execute("""UPDATE accounts
                                SET balance = balance + ?
                                WHERE account_id = ?;
                                """, (deposit_amount, account_to_deposit))
                    con.commit()
                    customer_accounts_menu(cust_user)

                elif account_choice == 'b':

                    account_to_withdraw = input("Which Account ID would you like to withdraw from? : ")
                    withdraw_amount = input("How much would you like to withdraw? : ")
                    cur.execute("""UPDATE accounts
                                SET balance = balance - ?
                                WHERE account_id = ?;
                                """, (withdraw_amount, account_to_withdraw))
                    con.commit()
                    customer_accounts_menu(cust_user)

                elif account_choice == 'c':
                    print("\nWould you like to Add or delete an account")
                    print("1. Add account 2. Delete account")
                    delete_or_add = input("Enter your choice (1 or 2): ")
                    
                    if delete_or_add == '1':
                        print("What type of account would you like to create")
                        type_of_acc = input("Please enter 'Savings' or 'Checking': ")
                        opened_date = datetime.datetime.now().strftime("%m/%d/%Y")
                        id_to_create = cur.execute("SELECT max(account_id) FROM accounts").fetchone()[0] + 1
                        cur.execute("INSERT INTO accounts (account_id, customer_id, account_type, balance, opened_on) VALUES (?,?,?,0,?)", (id_to_create, cust_id,type_of_acc, opened_date))
                        con.commit()
                    elif delete_or_add == '2':
                        acct_to_del = input("Which account Id?: ")
                        cur.execute("DELETE FROM accounts WHERE account_id = ?;", (acct_to_del,))
                        con.commit()
                    customer_accounts_menu(cust_user)
                else:
                    print("Invalid input. Please enter a,b, or c: ")
        else:
            print("Invalid input. Please choose a or b")



def customer_loan_menu(cust_user):
    print("\n\nCurrent Loans: ")
    cust_id = cur.execute("SELECT customer_id FROM customers WHERE username = ?;", (cust_user,)).fetchone()[0]
    cur.execute("""SELECT loan_id, loan_type, principal_amount, interest_rate, start_date, end_date, status 
                FROM loans WHERE customer_id = ? ORDER BY principal_amount DESC;""", (cust_id,))

    results = cur.fetchall()
    if results:
        for row in results:
            print(f"Loan ID: {row[0]} Loan Type: {row[1]}, Principal Amonunt: {row[2]}, Interest Rate: {row[3]}")
            print(f"Created on: {row[4]}, Ends on: {row[5]}, Status of loan: {row[6]}")
    else:
        print("Error fetching data")

    while True:
        print("\nChoose an option:")
        print("a. Go back")

        choice = input("Enter your choice (a): ")

        if choice == 'a':
            main_menu(cust_user)
        else:
            print("Invalid input. Please choose a or b")

if __name__ == "__main__":
    main_menu(login_check())
    