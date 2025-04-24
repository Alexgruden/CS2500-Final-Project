import pandas as pd
import csv
import sqlite3
import sys
import pwinput
import datetime


con = sqlite3.connect('bank_sim.db')

cur = con.cursor()


"""
Prompts user for username and password and verifies it within the database.
Continues prompting until correct credentials are entered and proceeds to main menu after.

Returns:
    str username: Returns the usename of the logged in user 
"""
def login_check():
    print("Welcome to Mini Bank ATM")
    while True:
        username = input("Username: ")
        password = pwinput.pwinput(prompt='Password: ')

        find_username = cur.execute("SELECT username FROM customers WHERE username = ?", (username,)).fetchone()
        if find_username:
            find_password = cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
            if find_password:
                print("successful login")
                return username
                main_menu(username)
            else:
                print("Access denied")






"""
Description:
When enabled, it will drop all current tables in the database and wipe what is in it.
Then it will recreate the tables as they were orgininally intended to be if needed.

Parameters:
input (boolean) : T/F Depending on if a fresh version of the database needs to be created
"""
def load_data(input):
    if input == True:
        #remove table during subsequent runs
        cur.execute("DROP TABLE IF EXISTS customers;")
        cur.execute("DROP TABLE IF EXISTS accounts;")
        cur.execute("DROP TABLE IF EXISTS loans;")

        #load each csv into a data frame
        customers = pd.read_csv("customers.csv")
        accounts = pd.read_csv("accounts.csv")
        loans = pd.read_csv("loans.csv")

        #insert each csv into a table in the database 
        customers.to_sql('customers', con, if_exists='replace', index = False)
        accounts.to_sql('accounts', con, if_exists='replace', index = False)
        loans.to_sql('loans', con, if_exists='replace', index = False)

        con.commit()
        con.close()


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
            print("a. Customers menu")
            print("b. Accounts menu")
            print("c. Loans menu")
            print("d. Logout")

            choice = input("Enter your choice (a,b,c, or d): ")

            if choice == 'a':
                print("You selected Option 1")
            elif choice == 'b':
                print("You selected Option 2")
            elif choice == 'c':
                print("You selected Option 3")
            elif choice == 'd':
                print("Exiting...")
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
            elif choice == 'b':
                print("You selected Option 2")
            elif choice == 'c':
                print("You selected Option 3")
            elif choice == 'd':
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid input. Please enter a,b,c, or d: ")


def admin_cust_menu(admin_user):

def admin_accounts_menu (admin_user):

def admin_loan_menu(admin_user):

def customer_cust_menu(cust_user):
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
                    query = f"UPDATE users SET {column_to_edit} = ? WHERE username = ?"
                    cur.execute(query, (change_to_column, cust_user))
                    con.commit()

        else:
            print("Invalid input. Please choose a or b")

def customer_accounts_menu (cust_user):
    print("Accounts :")
    cust_id = cur.execute("SELECT customer_id FROM customers WHERE username = ?;", (cust_user,)).fetchone()[0]
    cur.execute("SELECT account_id, account_type, balance, opened_on FROM accounts WHERE customer_id = ? ORDER BY posted_date ASC;", (cust_id,))

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
                    cur.execute("""UPDATE customers
                                SET balance = balace + ?
                                WHERE account_id = ?;
                                """, (deposit_amount, account_to_deposit))
                    con.commit()
                    customer_accounts_menu(cust_user)

                elif account_choice == 'b':

                    account_to_withdraw = input("Which Account ID would you like to withdraw from? : ")
                    withdraw_amount = input("How much would you like to withdraw? : ")
                    cur.execute("""UPDATE customers
                                SET balance = balace - ?
                                WHERE account_id = ?;
                                """, (withdraw_amount, account_to_deposit))
                    con.commit()
                    customer_accounts_menu(cust_user)

                elif account_choice == 'c':
                    print("Would you like to Add or delete an account")
                    print("1. Add account 2. Delete account")
                    delete_or_add = input("Enter your choice (1 or 2): ")
                    
                    if delete_or_add == 1:
                        print("What type of account would you like to create")
                        type_of_acc = input("Please enter 'Savings' or 'Checking': ")
                        opened_date = datetime.now().strftime("%m/%d/%Y")
                        id_to_create = cur.execute("SELECT max(account_id) FROM accounts")
                        cur.execute("INSERT INTO accounts (account_id, customer_id, account_type, balance, opened_on) VALUES (?,?,?,0,?)", (id_to_create, cust_user,type_of_acc, opened_date))
                        con.commit()
                    elif delete_or_add == 2:
                        acct_to_del = input("Which account Id?: ")
                        cur.execute("""DELETE FROM customers
                                    WHERE account_id = ?;
                                    """, (acct_to_del))
                        con.commit()
                    customer_accounts_menu(cust_user)
                else:
                    print("Invalid input. Please enter a,b, or c: ")
        else:
            print("Invalid input. Please choose a or b")
def customer_loan_menu(cust_user):