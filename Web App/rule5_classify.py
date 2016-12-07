
# coding: utf-8

# # Feature Engineering and Classification for Jargon Words

# In[3]:

import rule5_classify
from collections import Counter
from nltk.corpus import wordnet as wn
from nltk import word_tokenize
from random import shuffle
import pandas as pd
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.extmath import density
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import KFold
from sklearn.grid_search import GridSearchCV
from nltk.corpus import wordnet as wn
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion
from sklearn.externals import joblib


# In[4]:


def get_letter_combinations(candidate, features, number):
    candidate = candidate.replace(" ", "")
    if len(candidate) < number:
        return features
    else:
        for index in range(0, len(candidate), number):
            features[candidate[index:index + number]] += 1
        return features


# In[5]:

def generate_features(candidate):
    features = Counter()
#     print(candidate)
    candidate = str(str(candidate).lower().encode("ascii", "ignore"))
    features  = get_letter_combinations(candidate, features, 1)
    features  = get_letter_combinations(candidate, features, 2)
    features  = get_letter_combinations(candidate, features, 3)
    features  = get_letter_combinations(candidate, features, 4)
    features['first'] = candidate[:1]
#     features['second'] = word[1:2] # get the 'h' in Charlie?
    features['last_three'] = candidate[-3:]
    features['last_two'] = candidate[-2:]
    features['first_three'] = candidate[:3]
    features['name_len_id'] = len(candidate)
#     features['repeating_letters'] = get_first_repeating_letters(word)
#     features['continuous_vowels'] = get_first_repeating_vowels(word)
#     features['has_letters'] = has_letters(word, 'yzwx')
    return dict(features)
generate_features('veni vidi vici') 


# In[6]:


def get_wordnet_definition(candidate):
    words = word_tokenize(candidate)
    for word in words:
        synsets = wn.synsets(word)
        
    
    


# In[7]:

# This function allows experimentation with different feature definitions
# items is a list of (key, value) pairs from which features are extracted and training sets are made
# Feature sets returned are dictionaries of features

# This function also optionally returns the names of the training, development, 
# and test data for the purposes of error checking

def create_training_sets (feature_function, items, return_items=False):
    # Create the features sets.  Call the function that was passed in.
    # For names data, key is the name, and value is the gender
    shuffle(items)
    featuresets = [(feature_function(key), value, key) for (key, value) in items]
    
    # Divided training and testing in thirds.  Could divide in other proportions instead.
    fifth = int(float(len(featuresets)) / 5.0)
    
    train_set, dev_set, test_set = featuresets[0:fifth*4], featuresets[fifth*4:fifth*5], featuresets[fifth*4:]
    train_items, dev_items, test_items = items[0:fifth*4], items[fifth*4:fifth*5], items[fifth*4:]
    if return_items == True:
        return train_set, dev_set, test_set, train_items, dev_items, test_items
    else:
        return train_set, dev_set, test_set


# In[8]:

dataset_df = pd.read_csv("static/jargon_dataset.csv")


# In[9]:

items = []
for index in range(len(dataset_df)):
    items.append((dataset_df["Jargon_Terms"][index], dataset_df["is_Jargon"][index]))
    


# In[10]:

train_set, dev_set, test_set, train_items, dev_items, test_items = create_training_sets(generate_features, items, True)
# cl4 = nltk.NaiveBayesClassifier.train(train_set4)
# This is code from the NLTK chapter
errors = []
# print ("%.3f" % nltk.classify.accuracy(cl4, dev_set4))


# In[11]:

# print ("%.3f" % nltk.classify.accuracy(cl4, test_set4))
# print(train_set4[0][1])
# print(test_set4[:2])
test_set_features = np.asarray([item[0] for item in test_set])
train_set_features = np.asarray([item[0] for item in train_set])
test_set_names = np.asarray([item[2] for item in test_set])
train_set_names = np.asarray([item[2] for item in train_set])
test_set_labels = np.asarray([item[1] for item in test_set])
train_set_labels = np.asarray([item[1] for item in train_set])

train_set = {}
train_set["features"] = train_set_features
train_set["names"] = train_set_names
train_set["labels"] = train_set_labels

test_set = {}
test_set["features"] = test_set_features
test_set["names"] = test_set_names
test_set["labels"] = test_set_labels




# In[12]:

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


# In[13]:


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


# In[14]:

kaggle_classifier = Pipeline([('union', FeatureUnion(
                                    transformer_list=[

                                        # Pipeline for pulling features from the post's subject line
                                        ('names', Pipeline([
                                            ('selector', ItemSelector(key='names')),
                                            ('tfidf', TfidfVectorizer(analyzer='char', ngram_range=(2,3), sublinear_tf=True)),
                                        ])),

                                        # Pipeline for standard bag-of-words model for body
                                        ('features', Pipeline([
                                            ('selector', ItemSelector(key='features')),
                                            ('dict', DictVectorizer(sparse='False'))
                                        ])),

                                    ],

                                    # weight components in FeatureUnion
                                    transformer_weights={
                                        'names': 0.2,
                                        'features': 0.8,
                                    },
                                )),

                                # Use a SVC classifier on the combined features
                                ('svc', LinearSVC()),
                            ])
kaggle_classifier = kaggle_classifier.fit(train_set,train_set_labels)
    
kaggle_predictions = kaggle_classifier.predict(test_set)

accuracy_score(test_set_labels, kaggle_predictions)


# In[15]:

# kaggle_classifier.predict(["viz a viz", "tete a tete", "locker", "scrum", "scalar", "table"])
manual_list = [("dividend", True)]
manual_test_dict = create_manual_test_set(manual_list, generate_features)
manual_predictions = kaggle_classifier.predict(manual_test_dict)


# In[16]:

# kaggle_classifier = Pipeline([('tfidfvect', TfidfVectorizer(analyzer='char', ngram_range=(2,4), sublinear_tf=True)),
# #                                     ('feat',SelectKBest(chi2, 5)),
#                                     ('classifier', LinearSVC())
#                                    ])
# kaggle_classifier = kaggle_classifier.fit(train_set_names,train_set_labels)
    
# kaggle_predictions = kaggle_classifier.predict(test_set_names)

# accuracy_score(test_set_labels, kaggle_predictions)


# In[17]:

def test_manual_predictions(manual_list):
    manual_test_dict = create_manual_test_set(manual_list, generate_features)
    manual_predictions = kaggle_classifier.predict(manual_test_dict)
    
    


# In[18]:

# The True/False bit of the Tuple only needs to be accurate if you plan to test the accuracy using accuracy_score, 
# else it isn't considered.
manual_list = [("viz a viz", True), ("tete a tete",False), ("bottomline", True), ("ibuprofin", True), ("uninterested", False)]
test_manual_predictions(manual_list)


# In[20]:

def dump_stupid_pickle():
    joblib.dump(kaggle_classifier, 'static/linear_jargon_classifier.pkl') 


# In[21]:



