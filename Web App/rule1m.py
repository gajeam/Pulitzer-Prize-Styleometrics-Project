
# coding: utf-8

# ## The Notebook for Metaphors with an already trained classifier

# In[17]:

# get_ipython().magic('matplotlib inline')
import nltk
from nltk.corpus import names
import random
import pickle
from nltk.corpus import stopwords
import re
from nltk import trigrams


# In[ ]:




# In[18]:

def read_article_for_metaphor(article):
    f = open('static/my_classifier.pickle', 'rb')
    cl = pickle.load(f)
    f.close()
    
    testset = nltk.sent_tokenize(article)
    filtered_words = []
    testmeta = []
    word_list = ''
    para_index = 0
    #     text = ''.join(testset.readlines())
    #     sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)
    #     sentences = [t.rstrip() for t in sentences]
    #     print(sentences)
    for line in testset:
        para_index += 1
        word_list = line.split()
        filtered_words = [re.sub(r'[^\w\s]','',word.lower()) for word in word_list if word not in stopwords.words('english')]
        testmeta.append([' '.join(x) for x in trigrams(filtered_words)])
#         print(para_index)
    # print(testmeta)

    metaphor_count = 0
    nonmetaphor_count = 0
    metaphor_list = []
    for x in testmeta:
        for y in x:
            testsample = y
            print (testsample + ": " + cl.classify(metaphor_features(testsample)))
            if cl.classify(metaphor_features(testsample)) == 'metaphor':
                metaphor_count += 1
                metaphor_list.append(testsample)
            elif cl.classify(metaphor_features(testsample)) == 'NOT metaphor':
                nonmetaphor_count += 1
                
    return metaphor_list

#     print('metaphor_count:' + str(metaphor_count))
#     print('nonmetaphor_count:' + str(nonmetaphor_count))
#     print(metaphor_list)


# In[19]:

def create_regex_strings():
    stopwords_regex = "("
    # print(stopwords.words('english'))
    for word in stopwords.words('english'):
        stopwords_regex = stopwords_regex + word + "|"
    stopwords_regex = stopwords_regex[:-1] + "|an)"
#     print(stopwords_regex)
    punctuation_regex = r"[“”!\"#$%&'\(\)*+,-./:;<=>?@^_`{}~\s]*"
    return stopwords_regex, punctuation_regex



# In[22]:

def metaphor_features(word):
    features = {}
    word = word.lower()
    features['POS'] = word[0]
#     features['last'] = word[-1]
#     features['last 2'] = word[-2]
#     features['first 3'] = word[:3]
#     features['first'] = word[:1]
#     features['length'] = len(word)
#     features['starts with K'] = word.startswith('k')
#     features['ends with i'] = word.endswith('i')
#     features['ends with a'] = word.endswith('a')
#     features['double letter'] = double_letter(word)
    return features


# In[20]:

# with open("sciencearticle.txt", "r") as testset:
def rule1m_ranges_in_text(article):
    article = article.lower()
    word_list = ''
    highlight_bucket = []
    tag_list = []
    stopwords_regex, punctuation_regex = create_regex_strings()
    
    metaphor_list = read_article_for_metaphor(article)
    
    for trigram in metaphor_list:
#         print(trigram)
        trigram_list = trigram.split(" ")
        regex_string = "(" + trigram_list[0] + punctuation_regex + "(" + stopwords_regex + punctuation_regex + ")*" + trigram_list[1] + punctuation_regex + "(" + stopwords_regex + punctuation_regex + ")*" + trigram_list[2] + ")" 
#         print(regex_string)
#         print(article)
        match = re.search(regex_string, article)
        if match is not None:
            complete_trigram = match.group(0)
#             print(trigram, complete_trigram)
            index = article.find(complete_trigram)
#             print(index, complete_trigram)
            index_len = len(trigram)
            highlight_bucket.append(article[index:index+index_len])
            tag_list.append((index, index_len))
#             article = article[index+index_len:]
        else:
#              print("Not found: " + trigram)
             continue
    
        
    return tag_list

