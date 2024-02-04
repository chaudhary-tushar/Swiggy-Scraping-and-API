import requests
import time

from plyer import notification



url = "https://swiggy.com"
headers = {"User-Agent": "Mozilla/5.0 "
                        "(Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/114.0.0.0 Safari/537.3"}

while True :
    response = requests.get(url, headers=headers)
    if response.status_code != 403:
        print("here")
        notification.notify(
            title='Swiggy is Positive',
            message='Start the scraper',
        )
        break
    time.sleep(180)

