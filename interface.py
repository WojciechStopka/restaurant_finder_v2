import os
from functools import partial
from tkinter import *

from natsort import natsorted

from client import GoogleMapsClient


class RestaurantSearcherGUI:
    """
    A GUI application for finding restaurants based on user input.

    Attributes:
            window (Tk): The main window of the application.
            canvas (Canvas): The canvas for displaying the title.
            listbox (Listbox): The listbox for displaying restaurant search results.
            scrollbar (Scrollbar): The vertical scrollbar for the listbox.
            distance_entry (Entry): The entry field for specifying the distance from the user's location.
            city_entry (Entry): The entry field for specifying the user's current city.
            clicked_distance (int): The event ID for the click event on the distance entry.
            clicked_city (int): The event ID for the click event on the city entry.
            images (list): A list to store the image objects for the restaurant buttons.
            row (int): The current row position for placing buttons on the grid.
            column (int): The current column position for placing buttons on the grid.
    """

    def __init__(self):
        """
        Initializes the RestaurantSearcherGUI object and creates the interface for user.
        """
        self.window = Tk()
        self.window.title("Restaurant finder")
        self.window.geometry("800x850")
        self.window.config(bg="darkslategrey", pady=20)

        self.canvas = Canvas(
            self.window, width=800, height=100, bg="darkslategrey", highlightthickness=0
        )
        self.canvas.create_text(
            (400, 40),
            text="Restaurant finder",
            justify="center",
            font=("Arial", 30, "bold"),
            fill="white",
        )
        self.canvas.grid(column=0, columnspan=4, row=0)

        self.listbox = Listbox(
            self.window,
            bg="white",
            width=51,
            highlightthickness=5,
            highlightbackground="black",
            font=("Arial", 10, "bold"),
        )

        self.listbox.grid(column=1, columnspan=2, row=1)

        self.scrollbar = Scrollbar(
            self.window, orient="vertical", command=self.listbox.yview, width=15
        )
        self.scrollbar.grid(column=2, row=1, sticky="nes")

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.distance_entry = Entry(
            self.window,
            width=30,
            font=("Arial", 14, "bold"),
            highlightthickness=3,
            highlightbackground="black",
        )

        self.distance_entry.insert(0, "Radius (in KM)")
        self.distance_entry.grid(column=0, columnspan=2, row=2, pady=50, ipady=8)

        self.city_entry = Entry(
            self.window,
            width=30,
            font=("Arial", 14, "bold"),
            highlightthickness=3,
            highlightbackground="black",
        )
        self.city_entry.insert(0, "Location")
        self.city_entry.grid(column=2, columnspan=2, row=2, pady=50, ipady=8)

        self.clicked_distance = self.distance_entry.bind(
            "<Button-1>", self.clear_distance
        )
        self.clicked_city = self.city_entry.bind("<Button-1>", self.clear_city)

        self.images = []
        self.row = 3
        self.column = 0

        for image in natsorted(os.listdir("images")):
            image = image.replace(".png", "")
            img = PhotoImage(file=f"images/{image}.png")
            self.button = Button(
                self.window,
                text=image,
                image=img,
                highlightthickness=0,
                bg="black",
                compound="top",
                font=("Arial", 10, "bold"),
                fg="white",
                command=partial(self.get_locations, keyword=image),
            )
            self.button.grid(row=self.row, column=self.column, pady=(0, 20))
            self.images.append(img)
            self.column += 1
            if self.column == 4:
                self.row += 1
                self.column = 0
        self.window.mainloop()

    def clear_distance(self, event):
        """
        Clears the distance entry field when clicked by the user.

        Args:
                event (Event): The event object triggered by the click.
        """
        self.distance_entry.configure(state=NORMAL)
        self.distance_entry.delete(0, END)
        self.distance_entry.unbind("<Button-1>", self.clicked_distance)

    def clear_city(self, event):
        """
        Clears the city entry field when clicked by the user.

        Args:
                event (Event): The event object triggered by the click.
        """
        self.city_entry.configure(state=NORMAL)
        self.city_entry.delete(0, END)
        self.city_entry.unbind("<Button-1>", self.clicked_city)

    def get_locations(self, keyword):
        """
        Retrieves and displays restaurant search results in listbox based on user input.

        Args:
                keyword (str): The keyword representing the type of restaurant to search for.
        """
        self.listbox.delete("0", "end")
        client = GoogleMapsClient(self.city_entry.get(), keyword, self.distance_entry.get())
        client.extract_location()
        client.get_details()
        results = []
        for restaurant in client.restaurants:
            try:
                results.append(
                    f"{restaurant['name']} - rating: {restaurant['rating']} - votes: "
                    f"{restaurant['user_ratings_total']}"
                )
            except KeyError:
                continue
        self.listbox.insert(END, *results)
