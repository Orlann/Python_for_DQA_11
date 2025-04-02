import sys
import os
import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod  # For abstract base class
from datetime import datetime
# sys.path.append(r"C:\Users\anna_orlovska\Documents\OrlAnn\Epam\Python_for_DQA_11\Project\Python_for_DQA_11")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))     # adding one level up folder to sys.path
from Functions import case_correction
from Csv_files import *


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


class JsonInputHandler(InputHandler):
    def __init__(self):
        super().__init__()

    def get_string(self, prompt):
        """Default implementation for get_string."""
        return input(prompt)

    def get_float(self, prompt):
        """Default implementation for get_float."""
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid number. Please try again.")

    def get_date(self, prompt):
        """Default implementation for get_date."""
        while True:
            try:
                return datetime.strptime(input(prompt), "%d-%m-%Y")
            except ValueError:
                print("Invalid date format. Please use DD-MM-YYYY.")

    def get_json_path(self):
        """
        Decide whether to use a default file or request a custom file path.
        Returns the selected file path (default or user-provided).
        Loops until a valid file path is provided or user chooses to exit.
        """
        while True:
            use_default_file = input("Do you want to use the default JSON file ('json_messages.json')? (y/n): ").strip().lower()

            if use_default_file in ["y", "yes"]:
                json_path = "json_messages.json"  # Default file path
                print(f"Default file selected: {json_path}")
                return json_path
            elif use_default_file in ["n", "no"]:
                json_path = input("Enter the full JSON file path: ").strip()
                if os.path.exists(json_path):
                    print(f"Custom file selected: {json_path}")
                    return json_path
                else:
                    print(f"Error: File not found at '{json_path}'. Please provide a valid file path.")
            else:
                print("Invalid choice. Enter 'y' for default file or 'n' to provide a custom file path.")

    # JsonHandler-specific methods
    def load_json(self, json_path):
        # json_path = self.get_json_path()
        if not json_path:
            return  # Skip if no valid file path

        try:
            with open(json_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"Error: File '{json_path}' not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: Could not parse JSON in '{json_path}'.")
            return None

    def json_get_message(self, data):
        if isinstance(data, list):
            data_to_message = data
        elif isinstance(data, dict):
            data_to_message = [data]
            print(data_to_message)
        else:
            data_to_massage = []
            print('another data type')
        for message in data_to_message:
            message_type = message.get('type')
            if message_type.lower() == 'news':
                self.create_news(message.get('text'), message.get('add_parameter'))
            elif message_type.lower() == 'private add':
                self.create_private_add(message.get('text'), datetime.strptime(message.get('add_parameter'), "%d-%m-%Y"))
            elif message_type.lower() == 'sale':
                self.create_sale(message.get('text'), float(message.get('add_parameter')))
            else:
                return

    def handle_json_input(self):
        json_path = self.get_json_path()
        data = self.load_json(json_path)
        self.json_get_message(data)

        try:
            os.remove(json_path)
            print(f"\nInput file '{json_path}' has been deleted.")
        except Exception as e:
            print(f"Error: Unable to delete the file '{json_path}'. Reason: {e}")


class XmlInputHandler(InputHandler):
    def __init__(self):
        super().__init__()

    def get_string(self, prompt):
        """Default implementation for get_string."""
        return input(prompt)

    def get_float(self, prompt):
        """Default implementation for get_float."""
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid number. Please try again.")

    def get_date(self, prompt):
        """Default implementation for get_date."""
        while True:
            try:
                return datetime.strptime(input(prompt), "%d-%m-%Y")
            except ValueError:
                print("Invalid date format. Please use DD-MM-YYYY.")

    def get_xml_path(self):
        """
        Decide whether to use a default file or request a custom file path.
        Returns the selected file path (default or user-provided).
        Loops until a valid file path is provided or user chooses to exit.
        """
        while True:
            use_default_file = input("Do you want to use the default XML file ('xml_messages.xml')? (y/n): ").strip().lower()

            if use_default_file in ["y", "yes"]:
                xml_path = "xml_messages.xml"  # Default file path
                print(f"Default file selected: {xml_path}")
                return xml_path
            elif use_default_file in ["n", "no"]:
                xml_path = input("Enter the full XML file path: ").strip()
                if os.path.exists(xml_path):
                    print(f"Custom file selected: {xml_path}")
                    return xml_path
                else:
                    print(f"Error: File not found at '{xml_path}'. Please provide a valid file path.")
            else:
                print("Invalid choice. Enter 'y' for default file or 'n' to provide a custom file path.")

    # XmlHandler-specific methods
    def load_xml(self, xml_path):
        if not xml_path:
            return  # Skip if no valid file path

        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            return root
        except FileNotFoundError:
            print(f"Error: File '{xml_path}' not found.")
            return None
        except ET.ParseError:
            print(f"Error: Failed to parse XML in file '{xml_path}'. Make sure the file is well-formed.")

    def xml_get_message(self, root):
        if root is None:
            print("Error: no XML root element found")
            return []

        for element in root:
            message_type = element.tag

            if message_type.lower() == 'news':
                text = element.find("text").text if element.find("text") is not None else "Default News Text"
                city = element.find("city").text if element.find("city") is not None else "Default City"
                self.create_news(text, city)

            elif message_type.lower() == 'privateadd':
                text = element.find('text').text if element.find('text') is not None else 'Default Private Ad Text'
                expiration_date_str = element.find('expiration_date').text if element.find('expiration_date') is not None else '01-01-2025'
                try:
                    expiration_date = datetime.strptime(expiration_date_str, "%d-%m-%Y")
                except ValueError:
                    expiration_date = datetime.now()  # Default to current date if invalid
                self.create_private_add(text, expiration_date)

            elif message_type.lower() == 'sale':
                text = element.find('text').text if element.find('text') is not None else 'Default Sale Text'
                try:
                    price = float(element.find('price').text) if element.find('price') is not None else 0.0
                except ValueError:
                    price = 0.0  # Default to 0 if invalid
                self.create_sale(text, price)

            else:
                print(f"Unknown message type: '{message_type}'. Skipping element.")

        # return messages
    #
    def handle_xml_input(self):
        xml_path = self.get_xml_path()
        root = self.load_xml(xml_path)
        self.xml_get_message(root)

        try:
            os.remove(xml_path)
            print(f"\nInput file '{xml_path}' has been deleted.")
        except Exception as e:
            print(f"Error: Unable to delete the file '{xml_path}'. Reason: {e}")


def main():
    input_source = int(input("Choose input source \n1 - console\n2 - text file\n3 - JSON\n4 - XML\n").strip())
    if input_source == 1:
        handler = ConsoleInputHandler()
        handler.create_message()
    elif input_source == 2:
        file_handler = FileInputHandler()
        file_handler.handle_file_input()
    elif input_source == 3:
        json_handler = JsonInputHandler()
        json_handler.handle_json_input()
    elif input_source == 4:
        xml_handler = XmlInputHandler()
        xml_handler.handle_xml_input()

    # Added functionality from module 'CSV-files'
    input_list = read_from_file('output_messages.txt')
    count_dict = words_count(input_list)
    write_to_csv_without_header(count_dict)
    letters_statistic = letter_count(input_list)
    write_to_csv_with_header(letters_statistic)


if __name__ == "__main__":
    main()
