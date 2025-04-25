import sqlite3
import pandas as pd

con = sqlite3.connect('bank_sim.db')

cur = con.cursor()

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

if __name__ == "__main__":
    load_data(True)