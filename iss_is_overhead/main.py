import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = ""  # your email goes here
MY_PASS = ""  # your email password goes here
MY_LAT = 51.507351  # Your latitude
MY_LONG = -0.127758  # Your longitude

# access iss api endpoint
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

# get iss location
iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# parameters for sunrise and sunset api
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

# get times for sun rise and sunset using api
response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

# get current time
time_now = datetime.now().hour


#If the ISS is close to my current position,
# and it is currently dark
# Then email me to tell me to look up.
# run the code every 60 seconds.

def is_iss_overhead():
    # give margin of error for lat and long by +-5
    lower_lat = MY_LAT - 5
    upper_lat = MY_LAT + 5
    lower_lng = MY_LONG - 5
    upper_lng = MY_LONG + 5

    # if iss is in my vicinity, and it is dark, send email notifying me that the iss is overhead
    if lower_lat <= iss_latitude <= upper_lat and lower_lng <= iss_longitude <= upper_lng:
        if sunset <= time_now <= sunrise:
            return True


while True:
    time.sleep(60)
    if is_iss_overhead():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASS)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:Look Up\n\nThe ISS is above you in the sky."
        )
