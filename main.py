import time

import requests
from datetime import datetime
import smtplib

my_email = "baz.angra2@gmail.com"
password = "dmhmicwkfjniuyce"

MY_LAT = 80.000
MY_LONG = -345.000

# longitude = response.json()["iss_position"]["longitude"]
# latitude = response.json()["iss_position"]["latitude"]
#
# iss_position = (longitude, latitude)
#
# print(iss_position)

def is_iss_near():
    response1 = requests.get(url="http://api.open-notify.org/iss-now.json")
    response1.raise_for_status()
    data1 = response1.json()
    iss_latitude = float(data1["iss_position"]["latitude"])
    iss_longitude = float(data1["iss_position"]["longitude"])
    print(iss_latitude)
    print(iss_longitude)
    if (iss_latitude - 5 <= MY_LAT <= iss_latitude + 5) and (iss_longitude - 5 <= MY_LONG <= iss_longitude + 5):
        return True

def is_dark():
    parameters = {"lat": MY_LAT, "lng": MY_LONG, "formatted": 0}
    response2 = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response2.raise_for_status()
    data2 = response2.json()
    sunrise = int(data2["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data2["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now()
    hour = int(1)
    if sunset <= hour or hour <= sunrise:
        return True

while True:
    time.sleep(5)
    if is_iss_near() and is_dark():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="tania.varsh@gmail.com",
                msg="Subject:Train Times\n\nShould have taken the 10:30"
            )

# response1 = requests.get(url="http://api.open-notify.org/iss-now.json")
# response1.raise_for_status()
# data1 = response1.json()
# iss_latitude = float(data1["iss_position"]["latitude"])
# iss_longitude = float(data1["iss_position"]["longitude"])
# print(iss_latitude)
# print(iss_longitude)