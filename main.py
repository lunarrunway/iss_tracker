import requests
from datetime import datetime
import smtplib
import threading
import math

GMAIL_EMAIL = "bradj8184@gmail.com"
GMAIL_SMTP = "xmuk ctnt sesv dgjr"
YAHOO_EMAIL = "lunarrunway@yahoo.com"

COUNTDOWN = 60

NANAIMO_LAT = 49.164379
NANAIMO_LNG = -123.936661
nanaimo_parameters = {
    "lat": NANAIMO_LAT,
    "lng": NANAIMO_LNG,
    "formatted": 0
}


def is_night():
    time_now = int(datetime.now().hour)
    daylight_hours = requests.get(url="https://api.sunrisesunset.io/json", params=nanaimo_parameters)
    sunrise = int(daylight_hours.json()["results"]["sunrise"].split(":")[0])
    sunset = int(daylight_hours.json()["results"]["sunset"].split(":")[0]) + 12
    if time_now >= sunset or time_now <= sunrise:
        return True
    else:
        return False


def check_position():
    global t
    is_dark = is_night()
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_latitude = float(iss_response.json()["iss_position"]["latitude"])
    iss_longitude = float(iss_response.json()["iss_position"]["longitude"])
    iss_position = (iss_latitude, iss_longitude)
    my_position = (NANAIMO_LAT, NANAIMO_LNG)
    # print(f"lat_diff= {iss_position[0] - my_position[0]}, lon_diff= {iss_position[1] - my_position[1]}")
    if (math.isclose(a=iss_position[0], b=my_position[0], abs_tol=5)
            and math.isclose(a=iss_position[2], b=my_position[1], abs_tol=5)):
        if is_dark:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=GMAIL_EMAIL,
                                 password=GMAIL_SMTP)
                connection.sendmail(from_addr=GMAIL_EMAIL,
                                    to_addrs=YAHOO_EMAIL,
                                    msg="Subject: The ISS is near\n\n Go Look")
                print("email has been sent")
        else:
            t.cancel()
            timer()
            t.start()
    else:
        t.cancel()
        timer()
        t.start()


def timer():
    global t
    t = threading.Timer(COUNTDOWN, check_position)


timer()
check_position()
