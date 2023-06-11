import time
from tkinter import messagebox
from urllib.parse import urlencode

import requests

import creds


class GoogleMapsClient:
    """
    A class for interacting with a specific Google Maps API to retrieve restaurant data based on location, radius
    and keyword.

    Attributes:
            address (str): The address or name of the location.
            keyword (str): The keyword for filtering restaurant results.
            radius (int): The search radius in kilometers.
            lat (float): The latitude of the location.
            lng (float): The longitude of the location.
            api_key (str): The API key for accessing the API.
            data_type (str): The data type format for API responses.
            business_list (list): A list to store found restaurants.
            restaurants (list): A list to store chosen details of the restaurant.
    """

    def __init__(self, address, keyword, radius):
        """
        Initializes an instance of the ApiClient class.

        Args:
                address (str): The name of the location.
                keyword (str): The keyword for filtering restaurant results.
                radius (int): The search radius in kilometers.

        Raises:
                ValueError: If the radius value is not an integer.

        Example:
                client = ApiClient("New York City", "pizza", 5)
        """
        self.lat, self.lng = None, None
        try:
            self.radius = int(radius) * 1000
        except ValueError:
            messagebox.showerror(
                "Wrong distance", "Please provide correct number in distance box"
            )
        self.address = address
        self.keyword = keyword
        self.api_key = creds.api_key
        self.data_type = "json"
        self.business_list = []
        self.restaurants = []

    def extract_location(self):
        """
        Retrieves a longitude and latitude from geocode API by passed name of the location .
        """
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/{self.data_type}"
        params = {"address": self.address, "key": self.api_key}
        params_encoded = urlencode(params)
        url = f"{endpoint}?{params_encoded}"
        response = requests.get(url)
        if response.status_code not in range(200, 299):
            return messagebox.showerror("Error", "Can not access the server")
        try:
            location = response.json()["results"][0]["geometry"]["location"]
        except IndexError:
            return messagebox.showerror(
                "Wrong city error", "No results for passed city."
            )
        else:
            self.lat, self.lng = location["lat"], location["lng"]

    def get_nearby_places(self):
        """
        Retrieves all restaurants from nearbysearch API by passed params (keyword, location, opennow, radius, key).

        Returns:
                list: A list of dictionaries, each dictionary representing one result.
        """
        nearby_endpoint = (
            f"https://maps.googleapis.com/maps/api/place/nearbysearch/{self.data_type}"
        )
        nearby_params = {
            "keyword": self.keyword,
            "location": f"{self.lat}, {self.lng}",
            "opennow": True,
            "radius": self.radius,
            "key": self.api_key,
        }

        while len(self.business_list) < 60:
            time.sleep(0.2)
            nearby_params_encoded = urlencode(nearby_params)
            nearby_url = f"{nearby_endpoint}?{nearby_params_encoded}"
            nearby_response = requests.get(nearby_url)
            if nearby_response.status_code not in range(200, 299):
                return messagebox.showerror("Error", "Can not access the server")

            data = nearby_response.json()
            results = data["results"]
            self.business_list.extend(results)
            try:
                next_page_token = data["next_page_token"]
            except KeyError:
                return self.business_list
            else:
                nearby_params["pagetoken"] = next_page_token
        return self.business_list

    def get_details(self):
        """
        Retrieves chosen details about restaurants from details API by passed place_id param from get_nearby_places
        function.

        Returns:
                list: A list of dictionaries, each dictionary representing one restaurant.
        """
        details_endpoint = (
            f"https://maps.googleapis.com/maps/api/place/details/{self.data_type}"
        )
        for restaurant in self.get_nearby_places():
            details_params = {
                "place_id": restaurant["place_id"],
                "key": self.api_key,
                "fields": "formatted_address,name,rating,user_ratings_total",
            }
            details_params_encoded = urlencode(details_params)
            details_url = f"{details_endpoint}?{details_params_encoded}"
            details_response = requests.get(details_url)
            if details_response.status_code not in range(200, 299):
                return messagebox.showerror("Error", "Can not access the server")
            data = details_response.json()
            try:
                result = data["result"]
            except KeyError:
                continue
            else:
                self.restaurants.append(result)
        return self.restaurants
