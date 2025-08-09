import tkinter as tk
from tkinter import ttk, messagebox
import os

# Classes
class Hotel:
    sort_key = "name"

    def __init__(self, name, rooms, location, rating, price):
        self.name = name
        self.rooms = int(rooms)
        self.location = location
        self.rating = float(rating)
        self.price = float(price)

    def __lt__(self, other):
        return getattr(self, Hotel.sort_key) < getattr(other, Hotel.sort_key)

    def __repr__(self):
        return f"{self.name} | Rooms: {self.rooms} | {self.location} | Rating: {self.rating} | ₹{self.price}"

class User:
    def __init__(self, username, uid, cost, hotel_name):
        self.username = username
        self.uid = int(uid)
        self.cost = float(cost)
        self.hotel_name = hotel_name

    def __repr__(self):
        return f"{self.username} (ID: {self.uid}) - ₹{self.cost} at {self.hotel_name}"

# Load/Save
def load_hotels():
    hotels = []
    if os.path.exists("hotels.txt"):
        with open("hotels.txt") as f:
            for line in f:
                name, rooms, loc, rating, price = line.strip().split(",")
                hotels.append(Hotel(name, rooms, loc, rating, price))
    return hotels

def save_hotels(hotels):
    with open("hotels.txt", "w") as f:
        for h in hotels:
            f.write(f"{h.name},{h.rooms},{h.location},{h.rating},{h.price}\n")

def load_users():
    users = []
    if os.path.exists("users.txt"):
        with open("users.txt") as f:
            for line in f:
                name, uid, cost, hotel = line.strip().split(",")
                users.append(User(name, uid, cost, hotel))
    return users

def save_users(users):
    with open("users.txt", "w") as f:
        for u in users:
            f.write(f"{u.username},{u.uid},{u.cost},{u.hotel_name}\n")

def load_credentials():
    creds = {"owner": {}, "user": {}}
    if os.path.exists("credentials.txt"):
        with open("credentials.txt") as f:
            for line in f:
                role, username, password = line.strip().split(",")
                creds[role][username] = password
    return creds

# Login Window
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("600x600")
        self.creds = load_credentials()

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Label(self, text="Role").pack()
        self.role_cb = ttk.Combobox(self, values=["owner", "user"])
        self.role_cb.pack()
        self.role_cb.set("user")

        tk.Button(self, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_cb.get()

        if username in self.creds[role] and self.creds[role][username] == password:
            self.destroy()
            if role == "owner":
                OwnerDashboard().mainloop()
            else:
                UserDashboard().mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

# User Dashboard
class UserDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("User Dashboard")
        self.geometry("800x600")
        self.hotels = load_hotels()

        tk.Label(self, text="Available Hotels", font=("Arial", 14)).pack(pady=5)

        options = ["name", "rating", "rooms", "price"]
        self.sort_cb = ttk.Combobox(self, values=options)
        self.sort_cb.set("name")
        self.sort_cb.pack()
        tk.Button(self, text="Sort", command=self.sort_hotels).pack(pady=5)

        self.text = tk.Text(self, height=25, width=100)
        self.text.pack()
        self.display_hotels()

    def display_hotels(self):
        self.text.delete("1.0", tk.END)
        for h in self.hotels:
            self.text.insert(tk.END, str(h) + "\n")

    def sort_hotels(self):
        key = self.sort_cb.get()
        Hotel.sort_key = "rooms" if key == "rooms" else key
        self.hotels.sort()
        self.display_hotels()

# Owner Dashboard
class OwnerDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Owner Dashboard")
        self.geometry("800x700")
        self.hotels = load_hotels()
        self.users = load_users()

        tk.Label(self, text="Owner Dashboard", font=("Arial", 16)).pack(pady=5)

        self.text = tk.Text(self, height=15, width=100)
        self.text.pack()
        self.display_hotels()

        # Add hotel
        self.entries = {}
        frame = tk.LabelFrame(self, text="Add Hotel")
        frame.pack(pady=5, fill="x")
        for lbl in ["Name", "Rooms", "Location", "Rating", "Price"]:
            tk.Label(frame, text=lbl).pack()
            self.entries[lbl] = tk.Entry(frame)
            self.entries[lbl].pack()

        tk.Button(frame, text="Add Hotel", command=self.add_hotel).pack(pady=5)

        # Remove hotel
        tk.Label(frame, text="Remove Hotel (by name)").pack()
        self.remove_entry = tk.Entry(frame)
        self.remove_entry.pack()
        tk.Button(frame, text="Remove Hotel", command=self.remove_hotel).pack(pady=5)

        # User info
        self.user_text = tk.Text(self, height=10, width=100)
        self.user_text.pack()
        self.display_users()

        # Remove user
        tk.Label(self, text="Remove User (by ID)").pack()
        self.remove_user_entry = tk.Entry(self)
        self.remove_user_entry.pack()
        tk.Button(self, text="Remove User", command=self.remove_user).pack()

    def display_hotels(self):
        self.text.delete("1.0", tk.END)
        for h in self.hotels:
            self.text.insert(tk.END, str(h) + "\n")

    def display_users(self):
        self.user_text.delete("1.0", tk.END)
        for u in self.users:
            self.user_text.insert(tk.END, str(u) + "\n")

    def add_hotel(self):
        try:
            name = self.entries["Name"].get()
            rooms = int(self.entries["Rooms"].get())
            loc = self.entries["Location"].get()
            rating = float(self.entries["Rating"].get())
            price = float(self.entries["Price"].get())
            self.hotels.append(Hotel(name, rooms, loc, rating, price))
            save_hotels(self.hotels)
            self.display_hotels()
        except:
            messagebox.showerror("Error", "Invalid hotel input.")

    def remove_hotel(self):
        name = self.remove_entry.get()
        self.hotels = [h for h in self.hotels if h.name != name]
        save_hotels(self.hotels)
        self.display_hotels()

    def remove_user(self):
        try:
            uid = int(self.remove_user_entry.get())
            self.users = [u for u in self.users if u.uid != uid]
            save_users(self.users)
            self.display_users()
        except:
            messagebox.showerror("Error", "Invalid User ID.")

# Run the app
if __name__ == "__main__":
    LoginWindow().mainloop()
