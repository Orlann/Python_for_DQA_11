import sqlite3
import math


class CityDatabaseHandler:
    def __init__(self, db_name="city_coordinates.db"):
        self.db_name = db_name
        self.setup_database()

    def setup_database(self):
        """Create the database and table if they don't exist."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                name TEXT PRIMARY KEY,
                latitude REAL,
                longitude REAL
            )
        """)
        conn.commit()
        conn.close()

    def get_city_coordinates(self, city_name):
        """Retrieve city coordinates from the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT latitude, longitude FROM cities WHERE lower(name) = ?", (city_name.lower(),))
        result = cursor.fetchone()
        conn.close()
        return result

    def add_city_coordinates(self, city_name, latitude, longitude):
        """Add city coordinates to the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cities (name, latitude, longitude) VALUES (?, ?, ?)",
                       (city_name, latitude, longitude))
        conn.commit()
        conn.close()

    def get_table_data(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cities;")
        print(cursor.fetchall())
        conn.close()


class DistanceCalculator:
    def __init__(self, city_db):
        self.city_db = city_db  # Accept a CityDatabase object as a dependency

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        """Calculate the great-circle distance between two points on the Earth."""
        R = 6371  # Radius of the Earth in kilometers
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])  # Convert degrees to radians
        dist_lat = lat2 - lat1
        dist_lon = lon2 - lon1
        a = math.sin(dist_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dist_lon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def get_valid_coordinate(self, prompt, min_value, max_value):
        while True:
            try:
                value = float(input(prompt))
                if min_value <= value <= max_value:
                    return value
                else:
                    print(f"Please enter a value between {min_value} and {max_value}.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

    def get_or_add_city_coordinates(self, city_name):
        """Retrieve city coordinates or prompt the user to add them if not found."""
        coordinates = self.city_db.get_city_coordinates(city_name)
        if not coordinates:
            print(f"Coordinates for {city_name} not found.")
            latitude = self.get_valid_coordinate(f"Enter latitude for {city_name} (between -90 and 90): ", -90, 90)
            longitude = self.get_valid_coordinate(f"Enter longitude for {city_name} (between -180 and 180): ", -180, 180)
            self.city_db.add_city_coordinates(city_name, latitude, longitude)
            coordinates = (latitude, longitude)
        return coordinates

    def calculate_distance(self):
        """Main function to calculate the distance between two cities."""
        city1 = input("Enter the name of the first city: ").strip()
        city2 = input("Enter the name of the second city: ").strip()

        # Get coordinates for both cities
        coordinates1 = self.get_or_add_city_coordinates(city1)
        coordinates2 = self.get_or_add_city_coordinates(city2)

        # Calculate the distance
        distance = self.haversine(coordinates1[0], coordinates1[1], coordinates2[0], coordinates2[1])
        print(f"The straight-line distance between {city1} and {city2} is {distance:.2f} kilometers.\n")


if __name__ == "__main__":
    city_db = CityDatabaseHandler()
    calculator = DistanceCalculator(city_db)
    calculator.calculate_distance()
    city_db.get_table_data()        # check data in DB
