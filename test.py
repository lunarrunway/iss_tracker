from datetime import datetime
import requests
import smtplib

GMAIL_EMAIL = "bradj8184@gmail.com"
GMAIL_SMTP = "xmuk ctnt sesv dgjr"
YAHOO_EMAIL = "lunarrunway@yahoo.com"


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
    print(f"Time now hour: {time_now}\n Sunset Hour: {sunset}\n Sunrise Hour: {sunrise}")
    if time_now >= sunset or time_now <= sunrise:
        print("it's dark")
        return True
    else:
        print("it's not dark")
        return False


# with smtplib.SMTP("smtp.gmail.com") as connection:
#     connection.starttls()
#     connection.login(user=GMAIL_EMAIL,
#                      password=GMAIL_SMTP)
#     connection.sendmail(from_addr=GMAIL_EMAIL,
#                         to_addrs=YAHOO_EMAIL,
#                         msg="Subject: The ISS is near\n\n Go Look")
#     print("email has been sent")
is_night()
