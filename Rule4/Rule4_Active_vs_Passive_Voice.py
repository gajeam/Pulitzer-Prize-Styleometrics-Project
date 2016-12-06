
# coding: utf-8

# # Rule 4: Never use the passive where you can use the active.
# 
# We are using the dependency parser from Spacy to check for clauses, nouns and verbs which are tagged with a "passive tag". We are simply calculating the number of occurences of sentences that are in the passive voice and returning a decimal number denoting the percentage of articles in the article that are in the passive voice.

# In[18]:

from spacy.en import English


# In[17]:

def remove_quotes_from_text(text):
    # Check for all types of quotes
    import re
    quote_regex = r'"(.*?)"|“(.*?)”'
    text = re.sub(quote_regex, '', text)
    return text

def find_passive_percentage(article):
    '''This function accepts a string of sentences and prints them out classifying them into active or passive.    It returns a list of tuples in the format (starting_char_of_passive_sentence, length_of_passive_sentence)    of sentences that are passive.''' 

    parser = English()
    article = remove_quotes_from_text(article)
    
    parse = parser(article)

    passive_count = 0
    sentence_count = 0
    passive_list = []
    

    for sentence in parse.sents:
#         print(sentence)
        sent = str(sentence)
        hasPassive = False
        passive_indicators = []
        for word in sentence:
            if word.dep_ in ['nsubjpass', 'csubjpass', 'auxpass']:
                passive_indicators.append((word.dep_, word.text))
                hasPassive = True
        if hasPassive:
            passive_list.append((article.find(sent), len(sent)))
#             passive_count += 1
            print("Passive Voice Sentence: {0}.\nPassive Voice indicators: {1}".format(sentence, passive_indicators))
        else:
            continue
#             print("Active Voice Sentence: {0}".format(sentence))
            
#         sentence_count += 1


#     print("The percentage of passive sentences in this article is {0}%".format(round(passive_count*100/sentence_count, 2)))
    return passive_list



# In[16]:

##Using same article as Gabe's Rule 3 to check my code

# with open('gladwell_latebloomers.txt', 'r') as f:
#     rule4_percentage = find_passive_percentage(f.read())
#     print(rule4_percentage)


# In[ ]:



