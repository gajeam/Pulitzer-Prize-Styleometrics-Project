
# coding: utf-8

# In[100]:

import rule5_classify
import nltk
import spacy
from sklearn.externals import joblib
import pickle as pickle
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion
from sklearn.externals import joblib
from collections import Counter
import numpy as np
from nltk import bigrams
from nltk import collocations
from nltk import trigrams
from nltk.corpus import stopwords
import re
from string import punctuation


# In[88]:
rule5_classify.dump_stupid_pickle()
def generate_features(candidate):
    features = Counter()
#     print(candidate)
    candidate = str(str(candidate).lower().encode("ascii", "ignore"))
    features  = get_letter_combinations(candidate, features, 1)
    features  = get_letter_combinations(candidate, features, 2)
    features  = get_letter_combinations(candidate, features, 3)
    features  = get_letter_combinations(candidate, features, 4)
#     features  = get_letter_combinations(candidate, features, 5)
    features['first'] = candidate[:1]
    features['last_three'] = candidate[-3:]
    features['last_two'] = candidate[-2:]
    features['first_three'] = candidate[:3]
    features['name_len_id'] = len(candidate)
    return dict(features)

def get_letter_combinations(candidate, features, number):
    candidate = candidate.replace(" ", "")
    if len(candidate) < number:
        return features
    else:
        for index in range(0, len(candidate), number):
            features[candidate[index:index + number]] += 1
        return features

def create_manual_test_set(manual_list, generate_features):
    manual_set = [(generate_features(key), value, key) for (key, value) in manual_list]
    test_set_features = np.asarray([item[0] for item in manual_set])
    test_set_labels = np.asarray([item[1] for item in manual_set])
    test_set_names = np.asarray([item[2] for item in manual_set])
    manual_set_dict = {}
    manual_set_dict["features"] = test_set_features
    manual_set_dict["names"] = test_set_names
    manual_set_dict["labels"] = test_set_labels
    return manual_set_dict

def test_manual_predictions(manual_list, clf):
    manual_test_dict = create_manual_test_set(manual_list, generate_features)
    manual_predictions = clf.predict(manual_test_dict)
    return manual_predictions

def create_regex_strings():
    stopwords_regex = "("
    # print(stopwords.words('english'))
    for word in stopwords.words('english'):
        stopwords_regex = stopwords_regex + word + "|"
    stopwords_regex = stopwords_regex[:-1] + "|an)"
#     print(stopwords_regex)
    punctuation_regex = r"[“”!\"#$%&'\(\)*+,-./:;<=>?@^_`{}~\s]*"
    return stopwords_regex, punctuation_regex



# In[89]:

class ItemSelector(BaseEstimator, TransformerMixin):
    """For data grouped by feature, select subset of data at a provided key.

    The data is expected to be stored in a 2D data structure, where the first
    index is over features and the second is over samples.  i.e.

    >> len(data[key]) == n_samples

    Please note that this is the opposite convention to scikit-learn feature
    matrixes (where the first index corresponds to sample).

    ItemSelector only requires that the collection implement getitem
    (data[key]).  Examples include: a dict of lists, 2D numpy array, Pandas
    DataFrame, numpy record array, etc.

    >> data = {'a': [1, 5, 2, 5, 2, 8],
               'b': [9, 4, 1, 4, 1, 3]}
    >> ds = ItemSelector(key='a')
    >> data['a'] == ds.transform(data)

    ItemSelector is not designed to handle data grouped by sample.  (e.g. a
    list of dicts).  If your data is structured this way, consider a
    transformer along the lines of `sklearn.feature_extraction.DictVectorizer`.

    Parameters
    ----------
    key : hashable, required
        The key corresponding to the desired value in a mappable.
    """
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
#         print(data_dict)
        return data_dict[self.key]


# In[111]:



def remove_overlapping_tags(tag_list):
    print(tag_list)
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
    print(tag_list)
    return tag_list

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def adjust_classifier_biases(prediction_results, manual_list):
    for word_index in range(len(manual_list)):
        words =  manual_list[word_index][0].strip()
        if prediction_results[word_index]:
            if words[:-2] == " s":
                prediction_results[word_index] = False
            if is_number(words.strip()):
                prediction_results[word_index] = False
    return prediction_results


def rule5_ranges_in_text(article):
    clf = joblib.load('static/linear_jargon_classifier.pkl')

    mngram_list_by_sent = []
    manual_list = []

    stopwords_regex, punctuation_regex = create_regex_strings()

    sentences = nltk.sent_tokenize(article)
    words = nltk.word_tokenize(article)
    ngram_list = []
    tag_list = []
    print(words)

    for sent in sentences:
        word_list = sent.split()
        filtered_words = [re.sub(r'[^\w\s]','',word.lower()) for word in word_list if word not in stopwords.words('english')]
        mngram_list_by_sent.append([' '.join(x) for x in bigrams(filtered_words)])

    for ngram_list in mngram_list_by_sent:
        for ngram in ngram_list:
            manual_list.append((ngram.lower(), True))

    # mngram_list_by_sent = [ngram for sublist in ngram_list for ngram in sublist]
    manual_list = [(re.sub(r'[^\w\s]',' ',ngram.lower()), True) for ngram in words if ngram not in punctuation and len(ngram) > 1 and re.sub(r'[^\w\s]',' ',ngram.lower()).split()[0] not in stopwords.words('english')]
#     manual_list = [("viz a viz", True), ("capablesomething",False), ("bottomline", True), ("ibuprofin", True), ("uninterested", False)]
    prediction_results = test_manual_predictions(manual_list , clf)

    draft_article = article.lower()
    padding = 0
    print(manual_list)

    prediction_results = adjust_classifier_biases(prediction_results, manual_list)
    for word_index in range(len(manual_list)):
        word = manual_list[word_index][0].split()[0]
        index = draft_article.find(word)
        if index == -1:
            if prediction_results[word_index]:
                print("Not Found: ", manual_list[word_index][0])
            continue
            # print("Not Found: ", word)
        padding += index + len(manual_list[word_index][0])
        draft_article = draft_article[index + len(manual_list[word_index][0]):]

        if prediction_results[word_index]:
            print(word)
            tag_list.append((padding - len(manual_list[word_index][0]), len(manual_list[word_index][0])))
    #         ngram_list = manual_list[word_index][0].split(" ")
    #         print(ngram_list)
    #         regex_string = "(" + ngram_list[0] + punctuation_regex + "(" + stopwords_regex + punctuation_regex + ")*" + ngram_list[1] + ")" #+ punctuation_regex + "(" + stopwords_regex + punctuation_regex + ")*" + trigram_list[2] + ")"
    # #         print(regex_string)
    # #         print(article)
    #         match = re.search(regex_string, draft_article)
    #         if match is not None:
    #             complete_ngram = match.group(0)
    # #             print(trigram, complete_trigram)
    #             index = draft_article.find(complete_ngram)
    # #             print(index, complete_trigram)
    #             index_len = len(complete_ngram)
    #             tag_list.append((index, index_len))
    # #             article = article[index+index_len:]
    #         else:
    # #              print("Not found: " + trigram)
    #              continue

        else:
            continue

    return remove_overlapping_tags(tag_list)


# In[112]:

# Rule5("The increasing time of your life. Is that allons-y or would you bonjour rather kill me too viz-a-viz")


# In[24]:

# clf = joblib.load('linear_jargon_classifier.pkl')


# In[ ]:




# In[ ]:
