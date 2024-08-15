## Flight Offers Search API
import os
import requests
import datetime as dt

AMADEUS_ENDPOINT_2 = "https://test.api.amadeus.com/v2/shopping/flight-offers"
API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]
## 30 분 마다 새로운 token을 받아야 함.
ACCESS_TOKEN = "tisGQKV66mnEJAp8iEKhioJ4w7Kv"

class FlightData:
    #This class is responsible for structuring the flight data.
    '''Flights from low-cost carriers are currently unavailable.
    Flights from American Airlines, Delta and British Airways are currently unavailable.'''

    def __init__(self, destination_code):

        self.DEPARTURE = "ICN"
        self.CURRENCY = "USD"
        self.MAX_OFFERS = "15"

        self.today = dt.date.today()
        self.tomorrow = self.today + dt.timedelta(days=1)

        self.params = {
            "originLocationCode": self.DEPARTURE,
            "destinationLocationCode": destination_code,
            "departureDate": self.tomorrow,
            "adults": 1,
            "travelClass": "ECONOMY",
            "nonStop": "false",
            "currencyCode": self.CURRENCY,
            "max": self.MAX_OFFERS,
        }

        self.headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }

        response = requests.get(url=AMADEUS_ENDPOINT_2, params=self.params, headers=self.headers)
        self.ticket_list = response.json()["data"]
        self.price_list = []


    def cheapest_ticket(self):

        try:
            for ticket in self.ticket_list:
                total_price = float(ticket["price"]["grandTotal"])
                self.price_list.append(total_price)

            lowest_price = min(self.price_list)

        except ValueError:
            print("There's no flight tickets for tomorrow.")
            pass

        else:
            lowest_price_index = self.price_list.index(lowest_price)
            lowest_price_ticket = self.ticket_list[lowest_price_index]
            # print(price_list)
            # print(lowest_price_ticket)
            # print("--------------------")
            return lowest_price_ticket

    def lowest_price(self):
        try:
            for ticket in self.ticket_list:
                total_price = float(ticket["price"]["grandTotal"])
                self.price_list.append(total_price)

            lowest_price = min(self.price_list)

        except ValueError:
            print("There's no flight tickets for tomorrow.")
            return None

        else:
            return lowest_price







