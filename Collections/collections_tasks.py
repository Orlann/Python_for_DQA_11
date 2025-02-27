import random
import string

# Create a list with 2-10 dictionaries. Each dictionary has 3-15 items with letters as keys and numbers from 0 to 100 as values.
dict_list = [{random.choice(string.ascii_lowercase): random.randint(0, 100) for _ in range(random.randint(3, 15))} for _ in
             range(random.randint(2, 10))]

# Print all generated dictionaries
for i in dict_list:
    print(i)

# Max_records_dictionary is for all possible keys with (number of dictionary, max value, number of occurrence) tuple as values.
max_records_dictionary = {}
# Result_dictionary is for the final result
result_dictionary = {}

# Start from the 1st dictionary in the list
dict_number = 1
# Loop for all dictionaries in the list
for _ in range(len(dict_list)):
    # Loop for each item in the dictionary
    for key, value in dict_list[dict_number - 1].items():
        # Check if key appears for the first time
        if key not in max_records_dictionary:
            # Save firstly met key in the list
            max_records_dictionary[key] = (dict_number, value, 1)
        # Description of actions for already present key in the list
        else:
            # Increase count for this key
            count = max_records_dictionary[key][2] + 1
            # If new value is bigger then we save information about dictionary number with this value and count
            if value > max_records_dictionary[key][1]:
                max_records_dictionary[key] = (dict_number, value, count)
            # Else we keep information about previous dictionary number with this value and new count
            else:
                max_records_dictionary[key] = (max_records_dictionary[key][0], max_records_dictionary[key][1], count)
    # Move to the next dictionary in the list
    dict_number += 1

# Print dictionary with max value tuples
print(f"\nDictionary with max values:\n{max_records_dictionary}")

# Insert into the final dictionary necessary values
for key, value in max_records_dictionary.items():
    if value[2] == 1:
        result_dictionary[key] = value[1]
    else:
        result_dictionary[key + '_' + str(value[0])] = value[1]

# Print the final dictionary
print(f"\nFinal sorted dictionary:\n{dict(sorted(result_dictionary.items()))}")