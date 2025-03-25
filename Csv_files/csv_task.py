import csv
import re
from collections import Counter

path = r"C:\Users\anna_orlovska\Documents\OrlAnn\Epam\Python_for_DQA_11\Project\Python_for_DQA_11\Module_Files\output_messages.txt"


def read_from_file(input_file):
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return []


def write_to_csv_without_header(input_data):
    with open('word_count.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(input_data)


def write_to_csv_with_header(input_data):
    # Define the header
    header = ['letter', 'count_all', 'count_uppercase', 'percentage']

    with open('letter_count_csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(input_data)


def words_count(input_list):
    word_list = [word.replace(",", "")
                 for element in input_list
                 for word in element.strip().split()
                 if re.fullmatch(r'[a-zA-Z0-9-]*[a-zA-Z]+[a-zA-Z0-9-]*', word)
                 ]
    word_counts = dict(Counter(word_list))
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[0])
    return sorted_word_counts


def letter_count(input_list):
    letter_list = [char for string in input_list for char in string if char.isalpha()]
    small_letter_list = [letter.lower() for letter in letter_list]
    case_letter_count_dict = dict(Counter(letter_list))
    no_case_letter_count_dict = dict(Counter(small_letter_list))
    letter_statistic = []
    for letter, total_count in no_case_letter_count_dict.items():
        uppercase_letter = letter.upper()
        uppercase_count = case_letter_count_dict.get(uppercase_letter, 0)
        percentage_uppercase = round((uppercase_count / total_count) * 100, 2) if total_count > 0 else 0
        letter_statistic.append((uppercase_letter, total_count, uppercase_count, percentage_uppercase))
    return sorted(letter_statistic)


def main():
    input_list = read_from_file(path)
    count_dict = words_count(input_list)
    write_to_csv_without_header(count_dict)
    letters_statistic = letter_count(input_list)
    write_to_csv_with_header(letters_statistic)


if __name__ == "__main__":
    main()
