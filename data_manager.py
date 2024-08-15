## Airport & City Search API
from flight_data import FlightData
import requests
from twilio.rest import Client
import os
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']

SHEET_ENDPOINT = "https://api.sheety.co/b476c8b0a4b10bea8cdce84d6d411edb/flightDeals/prices"
# ADD sheety's token later. (as headers)

AMADEUS_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations"
API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]

# 30 분 마다 업데이트해야 하는 토큰
ACCESS_TOKEN = "tisGQKV66mnEJAp8iEKhioJ4w7Kv"

SHEET_TOKEN = {
    "Authorization": f"Bearer {os.environ['SHEET_TOKEN']}"
}

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.response = requests.get(url=SHEET_ENDPOINT, headers=SHEET_TOKEN)
        self.city_list = self.response.json()["prices"]
        self.n = 2

    def update(self):
        for city in self.city_list:
            city_name = city["city"]
            lowest_price_sheet = float(city["lowestPrice"])

            ## 막혔던 부분이 이거였구나..!!
            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}"
            }
            data = requests.get(url=f"{AMADEUS_ENDPOINT}?subType=CITY&keyword={city_name}"
                                f"&page%5Blimit%5D=10&page%5Boffset%5D=0&sort=analytics.travelers.score&view=FULL",
                                headers=headers)
            # print(data.json())
            city_code = data.json()["data"][0]["iataCode"]


            iata_json = {
                "price": {
                    "iataCode": city_code
                }
            }

            response = requests.put(url=f"{SHEET_ENDPOINT}/{self.n}", json=iata_json, headers=SHEET_TOKEN)
            print(response.text)
            self.n += 1

            cheapest_ticket = FlightData(destination_code=city_code).cheapest_ticket()
            cheapest_price_value = FlightData(destination_code=city_code).lowest_price()

            try:
                if lowest_price_sheet > cheapest_price_value:
                    ## Twilio SMS 전송
                    msg_body = (f"Beep🚨✨Cheapest✨ flight alert!\n Only ${cheapest_price_value} to fly from"
                                f" {FlightData(destination_code=city_code).DEPARTURE} to {city_code}, "
                                f"on {FlightData(destination_code=city_code).tomorrow}")

                    client = Client(account_sid, auth_token)

                    message = client.messages.create(
                        from_='+19787407091',
                        to='+821072049030',
                        body=msg_body,
                    )
                    # print(message.sid)

            except TypeError:
                '''When there's no flight tickets, the value of cheapest_price_value is going to be None(NoneType)
                and this will raise the TypeError.'''
                pass
            else:
                print("SMS alert sent!")






