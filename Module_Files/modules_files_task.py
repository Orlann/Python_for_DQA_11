import sys
import os
from abc import ABC, abstractmethod  # For abstract base class
from datetime import datetime
# sys.path.append(r"C:\Users\anna_orlovska\Documents\OrlAnn\Epam\Python_for_DQA_11\Project\Python_for_DQA_11")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))     # adding one level up folder to sys.path
from Functions import case_correction


class Massage:
    def __init__(self, text):
        self._text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, t):
        self._text = t

    def print_message(self):
        """Default implementation, can be overridden in subclasses."""
        print(f"{self.__class__.__name__} --------------")
        print(f"{self.text}")

    def save_to_file(self, file_name="output_messages.txt"):
        """Save the message text to a given .txt file."""
        with open('output_messages.txt', "a", encoding="utf-8") as file:
            file.write(f"{self.__class__.__name__} --------------\n")
            file.write(f"{self.text}\n")


class News(Massage):
    def __init__(self, city, text, date):
        super().__init__(text)
        self._city = city
        self._date = date

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, c):
        self._city = c

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, d):
        self._date = d

    def print_message(self):
        """News-specific print logic for News."""
        super().print_message()
        print(f"{self.city}, {self.date}")

    def save_to_file(self, file_name="output_messages.txt"):
        """Save News-specific details to the file."""
        with open(file_name, "a", encoding="utf-8") as file:
            file.write(f"News --------------\n")
            file.write(f"{self.text}\n")
            file.write(f"{self.city}, {self.date}\n\n")


class PrivateAdd(Massage):
    def __init__(self, text, expiration_date):
        super().__init__(text)
        self._expiration_date = expiration_date

    @property
    def expiration_date(self):
        return self._expiration_date

    @expiration_date.setter
    def expiration_date(self, ed):
        self._expiration_date = ed

    @property
    def remaining_days(self):
        """Calculate the remaining days until the expiration date."""
        today = datetime.now()
        difference = self._expiration_date - today
        return max(difference.days, 0)       # to avoid negative number

    def print_message(self):
        """News-specific print logic for Private Adds."""
        super().print_message()
        print(f"Actual until: {self.expiration_date.strftime('%d/%m/%Y')}, {self.remaining_days} days left")

    def save_to_file(self, file_name="output_messages.txt"):
        """Save PrivateAdd-specific details to the file."""
        with open(file_name, "a", encoding="utf-8") as file:
            file.write(f"Private Advertisement --------------\n")
            file.write(f"{self.text}\n")
            file.write(f"Actual until: {self.expiration_date.strftime('%d/%m/%Y')}, {self.remaining_days} days left\n\n")


class Sale(Massage):
    def __init__(self, text, price):
        super().__init__(text)
        self._price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, p):
        self._price = p

    @property
    def visa_discount(self):
        """Calculates discount for those who pays by Visa"""
        discount = self.price * 0.90
        return discount

    def print_message(self):
        """News-specific print logic for Message."""
        super().print_message()
        print(f"Price: {self.price} $, for Visa payment there is 10 % discount - price: {self.visa_discount} $")

    def save_to_file(self, file_name="output_messages.txt"):
        """Save Sale-specific details to the file."""
        with open(file_name, "a", encoding="utf-8") as file:
            file.write(f"Sale --------------\n")
            file.write(f"{self.text}\n")
            file.write(f"Price: {self.price} $, for Visa payment there is a 10% discount - price: {self.visa_discount} $\n\n")


class InputHandler(ABC):
    """General input handler for both console and file processing."""
    def __init__(self):
        pass

    @abstractmethod
    def get_string(self, prompt):
        """Abstract method to get a string input."""
        pass

    @abstractmethod
    def get_float(self, prompt):
        """Abstract method to get numerical input (float)."""
        pass

    @abstractmethod
    def get_date(self, prompt):
        """Abstract method to get date input."""
        pass

    def get_choice(self, choices, prompt="Choose an option: "):
        """Get a choice from a list of options."""
        while True:
            print(prompt)
            for i, choice in enumerate(choices, start=1):
                print(f"{i}. {choice}")
            try:
                selection = int(input("Enter the number of your choice: "))
                if 1 <= selection <= len(choices):
                    return choices[selection - 1]
                else:
                    print(f"Invalid choice. Please select a number between 1 and {len(choices)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def create_news(self, text, city):
        """Create and return a News object."""
        date = datetime.now()
        message = News(city=city, text=text, date=date.strftime("%d/%m/%Y %H:%M"))
        message.save_to_file()
        return message

    def create_private_add(self, text, expiration_date):
        """Create and return a PrivateAdd object."""
        message = PrivateAdd(text=text, expiration_date=expiration_date)
        message.save_to_file()
        return message

    def create_sale(self, text, price):
        """Create and return a Sale object."""
        message = Sale(text=text, price=price)
        message.save_to_file()
        return message


class ConsoleInputHandler(InputHandler):
    """Handle console-based input."""
    def __init__(self):
        super().__init__()
        print("Console Input Initialized!")

    def get_string(self, prompt="Enter a string: "):
        """Get a string input from the user."""
        return input(prompt)

    def get_float(self, prompt="Enter a number: "):
        """Get a float input from the user."""
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def get_date(self, prompt="Enter a date (DD-MM-YYYY): "):
        """Get a date input from the user."""
        while True:
            try:
                user_input = input(prompt)
                return datetime.strptime(user_input, "%d-%m-%Y")
            except ValueError:
                print("Invalid date format. Please use DD-MM-YYYY.")

    def get_choice(self, choices, prompt="Choose an option: "):
        return super().get_choice(choices, prompt)

    def create_message(self):
        """Create a message object based on user's choice."""
        message_type = self.get_choice(
            ["News", "Private ad", "Sale"],
            "What message type do you want to input?"
        )

        if message_type == "News":
            city = case_correction(self.get_string("Enter the city: "))
            text = case_correction(self.get_string("Enter the news text: "))
            return self.create_news(text, city)
        elif message_type == "Private ad":
            text = case_correction(self.get_string("Enter the advertisement text: "))
            expiration_date = self.get_date("Enter the expiration date (DD-MM-YYYY): ")
            return self.create_private_add(text, expiration_date)
        elif message_type == "Sale":
            text = case_correction(self.get_string("Enter the sale advertisement text: "))
            price = self.get_float("Enter the price: ")
            return self.create_sale(text, price)
        else:
            print("Invalid message type!")
            return None


class FileInputHandler(InputHandler):
    """Handle file-based input."""
    def __init__(self):
        super().__init__()  # No file path provided at initialization
        self.file_data = []  # Initialize an empty list for file data

    def get_file_path(self):
        """
        Decide whether to use a default file or request a custom file path.
        Returns the selected file path (default or user-provided).
        Loops until a valid file path is provided or user chooses to exit.
        """
        while True:
            use_default_file = input("Do you want to use the default file (input_messages.txt)? (y/n): ").strip().lower()

            if use_default_file in ["y", "yes"]:
                file_path = "input_messages.txt"  # Default file path
                print(f"Default file selected: {file_path}")
                return file_path
            elif use_default_file in ["n", "no"]:
                file_path = input("Enter the full file path: ").strip()
                if os.path.exists(file_path):
                    print(f"Custom file selected: {file_path}")
                    return file_path
                else:
                    print(f"Error: File not found at '{file_path}'. Please provide a valid file path.")
            else:
                print("Invalid choice. Enter 'y' for default file or 'n' to provide a custom file path.")

    def load_file(self, file_path):
        """
        Load the input file and return a list of lines.
        If the file is empty or corrupt, handle gracefully.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.readlines()
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return []

    def process_single_record(self):
        """
        Process only the first line of the file and create a single message object.
        Returns the created message object.
        """
        if not self.file_data:  # If no data is loaded, the file is empty
            print("Error: The file is empty.")
            return None

        line = self.file_data[0].strip()  # Process the first line
        components = line.split(",")
        if len(components) != 3:
            print(f"Skipping invalid record: {line}")
            return None

        message_type = components[0].strip()
        text = case_correction(components[1].strip())
        additional_param = components[2].strip()

        if message_type.lower() == "news":
            date = datetime.now().strftime("%d/%m/%Y %H:%M")  # Use the current date/time
            return News(city=case_correction(additional_param), text=text, date=date)

        elif message_type.lower() == "privatead":
            try:
                expiration_date = datetime.strptime(additional_param, "%d-%m-%Y")
                return PrivateAdd(text=text, expiration_date=expiration_date)
            except ValueError:
                print(f"Skipping invalid expiration_date: {additional_param}")
                return None

        elif message_type.lower() == "sale":
            try:
                price = float(additional_param)
                return Sale(text=text, price=price)
            except ValueError:
                print(f"Skipping invalid price: {additional_param}")
                return None

        print(f"Unknown message_type '{message_type}'")
        return None

    def process_multiple_records(self):
        """
        Process all lines in the file and create multiple message objects.
        Returns a list of created message objects.
        """
        messages = []
        if not self.file_data:  # If no data is loaded, the file is empty
            print("Error: The file is empty.")
            return []

        for line in self.file_data:
            line = line.strip()
            if not line:
                continue

            components = line.split(",")
            if len(components) != 3:
                print(f"Skipping invalid record: {line}")
                continue

            message_type = components[0].strip()
            text = case_correction(components[1].strip())
            additional_param = components[2].strip()

            if message_type.lower() == "news":
                date = datetime.now().strftime("%d/%m/%Y %H:%M")
                message = News(city=case_correction(additional_param), text=text, date=date)

            elif message_type.lower() == "privatead":
                try:
                    expiration_date = datetime.strptime(additional_param, "%d-%m-%Y")
                    message = PrivateAdd(text=text, expiration_date=expiration_date)
                except ValueError:
                    print(f"Skipping invalid expiration_date: {additional_param}")
                    continue

            elif message_type.lower() == "sale":
                try:
                    price = float(additional_param)
                    message = Sale(text=text, price=price)
                except ValueError:
                    print(f"Skipping invalid price: {additional_param}")
                    continue

            else:
                print(f"Unknown message_type '{message_type}'")
                continue

            # Save processed message to file
            message.save_to_file(file_name="output_messages.txt")
            messages.append(message)

        return messages

    def handle_file_input(self):
        """
        Process the file by asking whether it contains a single or multiple records.
        """
        # Call `get_file_path` to get the default or user-provided file path
        file_path = self.get_file_path()
        if not file_path:
            return  # Skip if no valid file path

        self.file_data = self.load_file(file_path)  # Load the file data
        if not self.file_data:  # Check for empty file
            print(f"Error: The file '{file_path}' is empty or could not be loaded.")
            return

        file_type = int(input("Does the file contain 1 record (1) or multiple records (2)? ").strip())

        if file_type == 1:
            message = self.process_single_record()
            if message:
                print("\nProcessed Single Record")
                message.save_to_file()
            else:
                print("\nNo valid record found.")
        elif file_type == 2:
            messages = self.process_multiple_records()
            print(f"\nProcessed {len(messages)} Records")
            for msg in messages:
                msg.save_to_file()
        else:
            print("Invalid choice!")

        try:
            os.remove(file_path)
            print(f"\nInput file '{file_path}' has been deleted.")
        except Exception as e:
            print(f"Error: Unable to delete the file '{file_path}'. Reason: {e}")

    def get_string(self, prompt=None):
        """Get the next string input from the file."""
        if not self.file_data:
            raise ValueError("No more data in the file.")
        return self.file_data.pop(0).strip()  # Remove and return the first line from the data

    def get_float(self, prompt=None):
        """Get the next float input from the file."""
        if not self.file_data:
            raise ValueError("No more data in the file.")
        try:
            return float(self.file_data.pop(0).strip())
        except ValueError:
            raise ValueError("The file does not contain a valid float.")

    def get_date(self, prompt=None):
        """Get the next date input from the file."""
        if not self.file_data:
            raise ValueError("No more data in the file.")
        try:
            return datetime.strptime(self.file_data.pop(0).strip(), "%d-%m-%Y")
        except ValueError:
            raise ValueError("The file does not contain a valid date in the format DD-MM-YYYY.")


def main():
    input_source = int(input("Choose input source (1 - console / 2 - file): ").strip())
    if input_source == 1:
        handler = ConsoleInputHandler()
        handler.create_message()
    elif input_source == 2:
        file_handler = FileInputHandler()
        file_handler.handle_file_input()


if __name__ == "__main__":
    main()
