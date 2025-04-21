import pandas as pd
import csv
import sqlite3

con = sqlite3.connect('bank_sim.db')

cur = con.cursor()

#remove table during subsequent runs
cur.execute("DROP TABLE IF EXISTS users;")
cur.execute("DROP TABLE IF EXISTS followers;")
cur.execute("DROP TABLE IF EXISTS posts;")

#load each csv into a data frame
users = pd.read_csv("users(in).csv")
followers = pd.read_csv("followers(in).csv")
posts = pd.read_csv("posts(in).csv")

#insert each csv into a table in the database 
users.to_sql('users', con, if_exists='replace', index = False)
followers.to_sql('followers', con, if_exists='replace', index = False)
posts.to_sql('posts', con, if_exists='replace', index = False)

con.commit()
con.close()


