import random
import string
import re

input_text_line = '''homEwork:
	tHis iz your homeWork, copy these Text to variable.

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
'''


def random_list_of_random_dictionaries(n: int, m: int, v: int) -> list:
    """
    Create a list of random number of dictionaries where each dictionary has random number of elements with alphabetic keys and
    values from 0 to random number.

    Parameters:
        n (int): max possible number of dictionaries in the list
        m (int): max possible number of elements in each dictionary
        v (int): max possible value of dictionary's values

    Returns:
        dict_list (list): list of random dictionaries
    """
    dict_list = [{random.choice(string.ascii_lowercase): random.randint(0, n) for _ in range(random.randint(3, m))} for _ in
             range(random.randint(2, v))]
    return dict_list


def find_max_values_in_dict_list(dict_list: list) -> dict:
    """
    Find max values in each dictionary in the list and create the list of max values.

    Parameters:
        dict_list(list): list of dictionaries

    Returns:
        result_dictionary(dictionary): dictionary with max value from each dictionary
    """
    max_records_dictionary = {}
    result_dictionary = {}

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
        # Insert into the final dictionary necessary values
        for key, value in max_records_dictionary.items():
            if value[2] == 1:
                result_dictionary[key] = value[1]
            else:
                result_dictionary[key + '_' + str(value[0])] = value[1]
    return result_dictionary


def split_text_into_lines(input_text: str) -> list:
    """
    Split the text into lines by new line symbol.

    Parameters:
        input_text(str): input text

    Returns:
        lines(list): list of input text lines
    """
    lines = input_text.split('\n')
    return lines


def split_list_elements_by_point(lines: list) -> list:
    """
    Split list elements by full stop symbol.

    Parameters:
        lines(list): input list of text lines

    Returns:
        sentences(list): list of lists of separate sentences
    """
    sentences = [line.split('. ') for line in lines]
    return sentences


def normalize_text(sentences: list) -> list:
    """
    Normalize text in terms of letter case.

    Parameters:
        sentences(list): input list of sentences

    Returns:
        cap_sentences(list): normalized list
    """
    cap_sentences = [[sentence.lstrip().capitalize() for sentence in sentence_list] for sentence_list in sentences]
    return cap_sentences


def case_correction(text):
    correct_text = text.lstrip().capitalize()
    return correct_text


def get_last_word(cap_sentences: list) -> list:
    """
    Get last word from every sentence.

    Parameters:
        cap_sentences(list): input list of sentences

    Returns:
        last_words(list): list of all last words
    """
    last_words_for_sentences = [[sentence.split()[-1].replace('.', '').replace(':', '').strip() if sentence else '' for sentence in
                             caps_sentence_in_list] for caps_sentence_in_list in cap_sentences]
    last_words = [word for word_list in last_words_for_sentences for word in word_list if word]
    return last_words


def create_sentence_from_list(last_words: list) -> list:
    """
    Create a sentence from all elements of the list.

    Parameters:
        last_words(list): input list of words

    Returns:
        last_sentence(str): sentence formed from all words of the input list
    """
    last_sentence = [' '.join(last_words)]
    return last_sentence


def join_text_from_list(cap_sentences: list) -> str:
    """
    Join all elements of the input list into text.

    Parameters:
        cap_sentences(list): input list of sentences

    Returns:
        last_sentence(str): sentence formed from all words of the input list
    """
    new_text = '\n'.join(['. '.join(''.join(sentence) for sentence in sublist) for sublist in cap_sentences]) + '.'
    return new_text


def correct_iz(new_text: str) -> str:
    """
    Replace all wrong 'iz' with 'is'.

    Parameters:
        new_text(str): input text

    Returns:
        correct_text(str): text with all wrong 'iz' replaced
    """
    correct_text = re.sub(r'\biz\b', 'is', new_text, flags=re.IGNORECASE)
    return correct_text


def space_count(correct_text: str) -> int:
    """
    Count all spaces in text.

    Parameters:
        correct_text(str): input text

    Returns:
        space_count(int): number of all spaces
    """
    spaces_number = sum(char.isspace() for char in correct_text)
    return spaces_number


print(f"\nNumber of spaces: {space_count}")


def main():
    # collections part
    rand_list_dict = random_list_of_random_dictionaries(3, 5, 100)
    print(f"\nRandom list of dictionaries:\n{rand_list_dict}")

    max_values = find_max_values_in_dict_list(rand_list_dict)
    print(f"\nFinal sorted dictionary:\n{dict(sorted(max_values.items()))}")

    # strings part
    lines = split_text_into_lines(input_text_line)
    sentences = split_list_elements_by_point(lines)
    cap_sentences = normalize_text(sentences)
    last_words = get_last_word(cap_sentences)
    last_sentence = create_sentence_from_list(last_words)
    cap_sentences.append(last_sentence)
    new_text = join_text_from_list(cap_sentences)
    correct_text = correct_iz(new_text)
    print(f"\nFinal correct text is:\n{correct_text}")

    print(f"\nNumber of spaces: {space_count(correct_text)}")


if __name__ == "__main__":
    main()



