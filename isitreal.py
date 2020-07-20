#Email Validation Check!
import requests

email_address = "test1231231@12312312.com"
response = requests.get("https://isitarealemail.com/api/email/validate",
    params = {'email': email_address})



if response.json()['status'] == "valid":
    print("This email address is Valid!")
else:
    print("This email address is Invalid!")
