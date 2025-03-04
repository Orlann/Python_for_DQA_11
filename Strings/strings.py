import re

input_text = '''homEwork:
	tHis iz your homeWork, copy these Text to variable.

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
'''

# Split the text into lines by new line symbol
lines = input_text.split('\n')

# Split lines into sentences by full stop symbol
sentences = [line.split('. ') for line in lines]

# Normalize sentences in terms of letter case
cap_sentences = [[sentence.lstrip().capitalize() for sentence in sentence_list] for sentence_list in sentences]

# Get last word from every sentence. Result list of lists where each inner list is list of last words for every sentence
last_words_for_sentences = [[sentence.split()[-1].replace('.', '').replace(':', '').strip() if sentence else '' for sentence in
                             caps_sentence_in_list] for caps_sentence_in_list in cap_sentences]

# Create general list of last words despite belonging to some sentence
last_words = [word for word_list in last_words_for_sentences for word in word_list if word]

# Create the last sentence
last_sentence = [' '.join(last_words)]

# Add last sentence to the list with all sentences
cap_sentences.append(last_sentence)

# Join the lines back together
new_text = '\n'.join(['. '.join(''.join(sentence) for sentence in sublist) for sublist in cap_sentences]) + '.'

# Replace wrong 'iz'
correct_text = re.sub(r'\biz\b', 'is', new_text, flags=re.IGNORECASE)
print(correct_text)

# Count spaces
space_count = sum(char.isspace() for char in correct_text)
print(f"\nNumber of spaces: {space_count}")
