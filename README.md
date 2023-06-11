# Restaurant_finder
![image](https://github.com/WojciechStopka/Restaurant_finder/assets/44327221/ac80b1e1-687f-42b5-b30e-d09a84069bf5)

The Restaurant Finder is a Python project that utilizes the Google Maps API to retrieve restaurant data based on location, radius, and keyword. It provides a GUI application for users to search for restaurants in given location.

## **Goals**
Within this project, I would like to explore the following:

- Getting to know Google Maps API documentation
- Practicing OOP
- Extracting specific data from Google Maps API
- Getting to know **requests** library and how to handle exceptions
- Creating simple and user-friendly GUI in **tkinter** library
- Making clear pop up's when user enter incorrect values


## Table of Contents

- [1. Installation](https://github.com/WojciechStopka/Restaurant_finder#1-instalation)
- [2. Authentication](https://github.com/WojciechStopka/Restaurant_finder#2-authentication)
- [3. Usage](https://github.com/WojciechStopka/Restaurant_finder#3-usage)
- [4. Example](https://github.com/WojciechStopka/Restaurant_finder#4-example)
- [5. Ideas for improvements](https://github.com/WojciechStopka/Restaurant_finder#5-ideas-for-improvements)
- [6. Project limitations](https://github.com/WojciechStopka/Restaurant_finder#6-project-limitations)

## 1. Installation
- Make sure you have Python 3.x installed on your system
- Clone the repository or download the code files from the GitHub repository
- Make sure **images** folder is in same directory as the script.
- Install the required libraries by running the following command
```
pip install requests urllib3 tkinter natsort
```
- Enable **[Geocoding API](https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com?project=python-places-api-386609)** and **[Places API](https://console.cloud.google.com/apis/library/places-backend.googleapis.com?project=python-places-api-386609)**
## 2. Authentication
To access the Google Maps API, you need to obtain an **API key** and store it in a file named **creds.py** in the same directory as the script. The API key is required for the code to function properly.
To create **API key** you should:
- Go to the Google Cloud Console.
- Create a new project or select an existing project.
- Enable the Google Maps Platform and generate an API key.
- Copy the API key and store it in a file named **creds.py** in the same directory as the script.


## 3. Usage
**To use the code, follow these steps:**
- Import the required module:
```
from Interface import RestaurantSearcherGUI
```
- Create an instance of the **Interface** class:
```
program = RestaurantSearcherGUI()
```
- Provide inormation in **Radius** and **Location** windows and choose type of food you are looking for.
  - In Location window, you can specify your location with information such as **city**, **street** and **building number**.
## 4. Example
![image](https://github.com/WojciechStopka/Restaurant_finder/assets/44327221/79702144-adb7-4706-939a-d54c8870cb9a)

## 5. Ideas for improvements

- Improving readability of listbox in GUI (when the name is too long, result goes out of the window, hiding all remaining informations)
- Sorting results by popularity/rating/votes etc... (Results are not displayed in any particular order)
- Enhancing utility of the project (for example: double-click on choosen record) that opens browser with direct link
- Making personalized "favorite places" section based on the location

## 6. Project limitations

- Google limit of maximum 60 results
- Lack of GUI responsiveness
- Only 12 types of food user can look for
