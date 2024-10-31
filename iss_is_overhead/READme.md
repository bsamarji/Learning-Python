# ISS tracking project
This python program tracks the location of the international space station (ISS) using API endpoints.
The program will send you an email if the ISS is above you in the sky and it is dark.

Before running the script you need to add your email and passwod to the constant variables at the top of the script.
```
import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = ""  # your email goes here
MY_PASS = ""  # your email password goes here
```

You might also need to change the smtp domain to fit your email domain. I used gmail as an example because it is popular:
```
connection = smtplib.SMTP("smtp.gmail.com")
```
