
# coding: utf-8

# # Rule 4: Never use the passive where you can use the active.
# 
# We are using the dependency parser from Spacy to check for clauses, nouns and verbs which are tagged with a "passive tag". We are simply calculating the number of occurences of sentences that are in the passive voice and returning a decimal number denoting the percentage of articles in the article that are in the passive voice.

# In[18]:
from spacy.en import English

parser = English()
# In[17]:
def rule4_ranges_in_text(article, parser):
    '''This function accepts a string of sentences and prints them out classifying them into active or passive.    It returns a list of tuples in the format (starting_char_of_passive_sentence, length_of_passive_sentence)    of sentences that are passive.''' 

    edited_article = remove_quotes_from_text(article)
    
    parse = parser(edited_article)
    
    passive_list = []
    

    for sentence in parse.sents:
        sent = str(sentence)
        hasPassive = False
        passive_indicators = []
        for word in sentence:
            if word.dep_ in ['nsubjpass', 'csubjpass', 'auxpass']:
                passive_indicators.append((word.dep_, word.text))
                hasPassive = True
        if hasPassive:
            passive_list.append((article.find(sent), len(sent)))
            print("Passive Voice Sentence: {0}.\nPassive Voice indicators: {1}".format(sentence, passive_indicators))
        else:
            continue
            
    return passive_list

def remove_quotes_from_text(text):
    # Check for all types of quotes
    import re
    quote_regex = r'"(.*?)"|“(.*?)”'
    text = re.sub(quote_regex, '', text)
    return text


