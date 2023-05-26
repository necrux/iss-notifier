#!/usr/bin/env python3
"""Check on the ISS and related methods."""
from datetime import datetime
import webbrowser
import requests

ISS_API = "http://api.open-notify.org/iss-now.json"
PEOPLE_API = "http://api.open-notify.org/astros.json"
SUN_API = "https://api.sunrise-sunset.org/json"


class ISS:
    """Check on the ISS and related methods."""

    def iss_coordinates(self) -> tuple:
        """Get the ISS' current location."""
        response = requests.get(url=ISS_API, timeout=5)
        response.raise_for_status()
        data = response.json()

        latitude = float(data["iss_position"]["latitude"])
        longitude = float(data["iss_position"]["longitude"])
        return latitude, longitude

    def is_iss_overhead(self, latitude, longitude) -> bool:
        """Check if the ISS is overhead (+/-5 degrees)."""
        iss_latitude, iss_longitude = self.iss_coordinates()

        # Your position is within +5 or -5 degrees of the ISS position.
        if latitude - 5 <= iss_latitude <= latitude + 5 and \
                longitude - 5 <= iss_longitude <= longitude + 5:
            return True
        return False

    def iss_current_location(self):
        """Get the current location of the ISS and open in a browser."""
        iss_latitude, iss_longitude = self.iss_coordinates()

        webbrowser.open(f"https://www.latlong.net/c/?lat={iss_latitude}&long={iss_longitude}")

    def people_aboard(self) -> list:
        """Get a list of the people currently aboard the ISS."""
        response = requests.get(url=PEOPLE_API, timeout=5)
        response.raise_for_status()
        data = response.json()
        people = [person["name"] for person in data["people"] if person["craft"] == "ISS"]
        return people

    @staticmethod
    def is_night(latitude, longitude) -> bool:
        """Check if it is nighttime at the provided coordinates."""
        parameters = {
            "lat": latitude,
            "lng": longitude,
            "formatted": 0,
        }

        response = requests.get(url=SUN_API, params=parameters, timeout=5)
        response.raise_for_status()
        data = response.json()
        sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
        sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

        time_now = datetime.now().hour

        if time_now >= sunset or time_now <= sunrise:
            return True
        return False
