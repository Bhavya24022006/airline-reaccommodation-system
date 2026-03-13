import pandas as pd

def load_data():
    airports = pd.read_csv("data/raw/airports.csv")
    flights = pd.read_csv("data/raw/flights.csv")
    passengers = pd.read_csv("data/raw/passengers.csv")
    pnr_bookings = pd.read_csv("data/raw/pnr_bookings.csv")
    schedule_changes = pd.read_csv("data/raw/schedule_changes.csv")
    schedules = pd.read_csv("data/raw/schedules.csv")
    seat_inventory = pd.read_csv("data/raw/seat_inventory.csv")
    
    return airports, flights, passengers, pnr_bookings, schedule_changes, schedules, seat_inventory