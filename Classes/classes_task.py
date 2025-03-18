from datetime import datetime


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

    def save_to_file(self, file_name="messages.txt"):
        """Save the message text to a given .txt file."""
        with open('messages.txt', "a", encoding="utf-8") as file:
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

    def save_to_file(self, file_name="messages.txt"):
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

    def save_to_file(self, file_name="messages.txt"):
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

    def save_to_file(self, file_name="messages.txt"):
        """Save Sale-specific details to the file."""
        with open(file_name, "a", encoding="utf-8") as file:
            file.write(f"Sale --------------\n")
            file.write(f"{self.text}\n")
            file.write(f"Price: {self.price} $, for Visa payment there is a 10% discount - price: {self.visa_discount} $\n\n")


class ConsoleInputHandler:
    def __init__(self):
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

    def confirm(self, prompt="Do you want to publish the message? (y/n): "):
        """Get a yes/no confirmation from the user."""
        while True:
            choice = input(prompt).strip().lower()
            if choice in ['y', 'yes']:
                # TODO
                # write to text file
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    def create_news(self):
        """
        Method to create a News object by getting the required input (city and text) from the user.
        """
        city = self.get_string("Enter the city: ")
        text = self.get_string("Enter the news text: ")
        date = datetime.now()
        date_formatted = date.strftime("%d/%m/%Y %H:%M")
        if self.confirm():
            message = News(city, text, date_formatted)
            message.save_to_file()
            return message

    def create_private_add(self):
        """Create a PrivateAdd object."""
        text = self.get_string("Enter the advertisement text: ")
        expiration_date = self.get_date("Enter the expiration date (DD-MM-YYYY): ")
        if self.confirm():
            message = PrivateAdd(text, expiration_date)
            message.save_to_file()
            return message

    def create_sale(self):
        """Create a Sale object."""
        text = self.get_string("Enter the sale advertisement text: ")
        price = self.get_float("Enter the price: ")
        if self.confirm():
            message = Sale(text, price)
            message.save_to_file()
            return message

    def create_message(self):
        """Create a message object based on user's choice."""
        message_type = self.get_choice(
            ["News", "Private ad", "Sale"],
            "What message type do you want to input?"
        )

        if message_type == "News":
            return self.create_news()
        elif message_type == "Private ad":
            return self.create_private_add()
        elif message_type == "Sale":
            return self.create_sale()
        else:
            print("Invalid choice!")
            return None


def main():
    console_handler = ConsoleInputHandler()

    message = console_handler.create_message()

    if message:
        message.print_message()
    else:
        print("\nNo valid message was created.")


if __name__ == "__main__":
    main()
