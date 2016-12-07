
# coding: utf-8

# In[100]:

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

def Rule5(article):
    clf = joblib.load('linear_jargon_classifier.pkl') 
    
    markup_list = []
    
    sentences = nltk.sent_tokenize(article)
    words = nltk.word_tokenize(article)
    ngram_list = []
    print(sentences)
    for sent in sentences:
        word_list = sent.split()
        filtered_words = [word.lower() for word in word_list] # if word.lower() not in stopwords.words('english')
        print(filtered_words)
        ngram_list.append([' '.join(x) for x in trigrams(filtered_words)])
    ngram_list = [ngram for sublist in ngram_list for ngram in sublist]
    print(ngram_list)
    manual_list = [(ngram.lower(), True) for ngram in words]# if ngram not in punctuation]
#     manual_list = [("viz a viz", True), ("capablesomething",False), ("bottomline", True), ("ibuprofin", True), ("uninterested", False)]
    prediction_results = test_manual_predictions(manual_list , clf)
    
    draft_article = article
    for word_index in range(len(words)):
        if prediction_results[word_index]:
            index = draft_article.find(words[word_index])
            markup_list.append((index, len(words[word_index])))
        else:
            continue
        draft_article = draft_article[len(words[word_index]):]
    
    return markup_list
            


# In[112]:

# Rule5("The increasing time of your life. Is that allons-y or would you bonjour rather kill me too viz-a-viz")


# In[24]:

# clf = joblib.load('linear_jargon_classifier.pkl') 


# In[ ]:




# In[ ]:



