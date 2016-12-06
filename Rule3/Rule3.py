
# coding: utf-8

# # Rule 3: If it is possible to cut a word out, always cut it out.
# 
# This list of unnecessary words comes from the Purdue Online Writing Lab articles on [eliminating words](https://owl.english.purdue.edu/owl/resource/572/02/) and [avoiding common pitfalls.](https://owl.english.purdue.edu/owl/resource/572/04/) Here, we are simply calculating the number of occurences of removable words and putting it in a nice data frame.

# In[1]:

import re
import pandas as pd
import pprint as pp
import sys

# In[2]:

def load_unnecesary_regexes():
    filename = sys.path[1] + '/Rule3/unnecessary_words.csv'
    try:
        f = open(filename)
    except:
        pp.pprint('Bad filename ' + filename)
        return None
    print('Loading unnecessary words...')
    words = f.read().split(',')
    return words

def regex_for_word(word):
    return word.replace('*', '[a-zA-Z]+')

# Save the regexes to find unnecessary words as a global variable
unnecessary_regexes = load_unnecesary_regexes()


# In[3]:

def remove_quotes_from_text(text):
    # Check for all types of quotes
    quote_regex = r'"(.*?)"|“(.*?)”'
    text = re.sub(quote_regex, '', text)
    return text

def find_phrases_in_text(text, phrases):
    phrase_list = []
    for phrase in phrases:
        phrase_count = len(re.findall(regex_for_word(phrase), text, flags=re.IGNORECASE))
        if phrase_count is not 0:
            phrase_list.append((phrase, phrase_count))
    return phrase_list

def unnecessary_phrase_count_in_text(text):
    text = remove_quotes_from_text(text)
    text_phrases = find_phrases_in_text(text, unnecessary_regexes)
    frame = pd.DataFrame(text_phrases)
    frame.columns = ['PHRASE', 'COUNT']
    return frame


# In[4]:

def rule3_ranges_in_text(text):
    phrase_location_list = []
    for phrase in unnecessary_regexes:
        phrase_matches = re.finditer(regex_for_word(phrase), text, flags=re.IGNORECASE)
        for phrase_match in phrase_matches:            
            phrase_location_list.append(phrase_match.span())
    return [(start, end - start) for (start, end) in phrase_location_list]

