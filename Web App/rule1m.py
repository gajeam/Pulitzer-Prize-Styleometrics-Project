
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

def remove_overlapping_tags(tag_list):
    # print(tag_list)
    index = 0
    while index < len(tag_list) - 1:
        potential_overlapping_index = index + 1
        # print(index)
        while potential_overlapping_index < len(tag_list):
            # print("in",potential_overlapping_index)
            if tag_list[index][0] + tag_list[index][1] > tag_list[potential_overlapping_index][0]:
                tag_list[index] = (tag_list[index][0], tag_list[potential_overlapping_index][0] + tag_list[potential_overlapping_index][1])
                # print("Remove: ", tag_list[potential_overlapping_index])
                tag_list.remove(tag_list[potential_overlapping_index])
            else:
                potential_overlapping_index += 1
                break
        index += 1
    # print(tag_list)
    return tag_list


# In[18]:

def read_article_for_metaphor(article):
    f = open('static/my_classifier.pickle', 'rb')
    cl = pickle.load(f)
    f.close()

    testset = nltk.sent_tokenize(article)
    # print(testset)
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

def metaphor_features(wordphrase):
    features = {}
    POS_bucket = []
    wordphrase = wordphrase.lower()
#     for line in wordphrase:
#         for word in line:
#             POS = nltk.pos_tag(word)
#             POS_bucket.append(POS[0][1])
    features = featurize_pos_list(get_pos_list_from_ngram(wordphrase), features)
    return features

def featurize_pos_list(pos_list, features):
    for pos in pos_list:
        if pos in features.keys():
            features[pos] += 1
        else:
            features[pos] = 1
    return features

def get_pos_list_from_ngram(ngram):
    ngram_tagged = nltk.pos_tag(ngram.split())
    pos_list = [tagged_word[1] for tagged_word in ngram_tagged]
    return pos_list


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
            index_len = len(complete_trigram)
            highlight_bucket.append(article[index:index+index_len])
            tag_list.append((index, index_len))
#             article = article[index+index_len:]
        else:
             print("Not found: " + trigram)
             continue


    return remove_overlapping_tags(tag_list)
