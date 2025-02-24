import copy
import random


def genarate_random_list(n, start, end):
    """
    Generate a list of 'n' random integers between 'start' and 'end'.

    Parameters:
    n (int): The number of random integers to generate.
    start (int): The lower bound for the random integers.
    end (int): The upper bound for the random integers.

    Returns:
    list: A list of 'n' random integers between 'start' and 'end'.
    """
    random_list = []
    random_list = [random.randint(start, end) for _ in range(n)]
    return random_list


def list_sorting(input_list):
    """
    Return sorted list.

    Parameters:
    input_list (list): The list of numbers to sort.

    Returns:
    list: A sorted list.
    """
    input_list_copy = copy.deepcopy(input_list)
    sorted_list = []
    while input_list_copy:
        min_value = input_list_copy[0]
        for i in range(len(input_list_copy)):
            if input_list_copy[i] < min_value:
                min_value = input_list_copy[i]
        sorted_list.append(min_value)
        input_list_copy.remove(min_value)
    return sorted_list


def find_odd_numbers(input_list):
    """
    Find and return all odd numbers in a list.

    Parameters:
    input_list (list): The list of numbers to check for odd numbers.

    Returns:
    list: A list of all odd numbers in the input list.
    """
    odd_list = [i for i in input_list if i % 2 == 1]
    return odd_list


def find_even_numbers(input_list):
    """
    Find and return all even numbers in a list.

    Parameters:
    input_list (list): The list of numbers to check for even numbers.

    Returns:
    list: A list of all even numbers in the input list.
    """
    even_list = [i for i in input_list if i % 2 == 0]
    return even_list


def list_average(input_list):
    """
    Calculate and return the average of a list.

    If the input list is empty, print an error message and return None.

    Parameters:
    input_list (list): The list of numbers to calculate the average of.

    Returns:
    float: The average of the input list, or None if the list is empty.
    """
    try:
        return sum(input_list) / len(input_list)
    except ZeroDivisionError:
        print("Error: Trying to find the average of an empty list.")
        return None


def main():
    # generate list of random numbers
    numbers = genarate_random_list(10, 0, 1000)
    print(f"Input list: {numbers}")

    # sort and output sorted list
    print(f"Sorted list: {list_sorting(numbers)}")

    # find and output all odd numbers and their average value
    odd_numbers = find_odd_numbers(numbers)
    print(f"Odd numbers: {odd_numbers}")
    print(f"Odd numbers average: {list_average(odd_numbers):.2f}")

    # find and output all even numbers and their average value
    even_numbers = find_even_numbers(numbers)
    print(f"Even numbers: {even_numbers}")
    print(f"Even numbers average: {list_average(even_numbers):.2f}")


if __name__ == "__main__":
    main()
