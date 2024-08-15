# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes
# to achieve the program requirements.
from data_manager import DataManager

'''First of all, visit Amadeus API and get a new access token (effectivity: only for 30 minutes)
Update the ACCESS_TOKEN constant in data_manager.py and flight_data.py each with the new token.
Otherwise, a KeyError will be raised.'''

DataManager().update()


