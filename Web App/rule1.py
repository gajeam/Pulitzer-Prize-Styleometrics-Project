
# coding: utf-8

# **the algorithm:**  
# take a big corpus with trite similes (Pulp Fiction collection, War and Peace, Romance books, [The Daily Mail](http://cs.nyu.edu/~kcho/DMQA/)), prepare clean sentences, traverce throug the corpus sen by sen, POS-tagging each and looking for sentences containing prepositions "like" and "as-as" (tag = "IN") and exclude "as soon as, as well as, as usual, such as, as of yet, as much, like that, like this.." (alternatively, use dependency parser to accurately cut out a phrase. but it's a pain and may be an overkill). Add these sentences to a target corpus. Cut out a simile candidate (segment of a sentence) out of each sentence; replace "likes" and "ases" with a "comparator".  
# Take a list of candidates and compare each of them to the rest of them. If 3 of 4 words match (75%), count this match as 1. All similes that match with other 5 similes are considered to be trite (5 is subjective; can put a higher num to get *really* trite similes; generally, the bigger the training set, the higher might be the number). Write all trite similes into a pkl-file. This is our collection. With a testing set, repeat all steps up to fuzzy matching. Then, instead of fuzzy matching candidates across the testing set, fuzzy match them with the trite similes collection. Output sentences that have a simile. For sents with trite simile - 'True', for sents with non-trite simile - 'False'.  
# **important: instal tqdm (pip tqdm install)** it will show the progress.
# 

# In[10]:

import nltk

min_simile_freq = 5
train_dir_name = 'C:/Users/Nat/Documents/_ANLP/Final_Project/training_data/' #REASSIGN
test_dir_name = 'C:/Users/Nat/Documents/_ANLP/Final_Project/pulitzer_testing_data/not_annotated' #REASSIGN


# from nltk.parse.stanford import StanfordDependencyParser
# path_to_jar = '/Development/Projects/Magnifis/3rd_party/NLU/stanford-corenlp-full-2013/stanford-corenlp-3.2.0.jar'
# path_to_models_jar ='/Development/Projects/Magnifis/3rd_party/NLU/stanford-corenlp-full-2013/stanford-corenlp-3.2.0-models.jar'
# dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

# result = dependency_parser.raw_parse('I shot an elephant in my sleep')
# dep = result.next()
# list(dep.triples())


# In[11]:

import os
import io
import codecs
import re


regex_filter = r"(as soon)|(as well)|(as if)|(as \w+ as possible)|(as before)|(as long)|(as usual)|(as ever)|(as a result)|(such as)|(as of yet)|(as much)|(as many)|(like that)|(like this)|(like you)|(like me)|(like him)|(like us)|(like her)|(look like)|(looks like)|(like everything else)|(like everyone else)|(anybody like)|(anyone like)"



# In[12]:

from tqdm import tqdm #visualization of the processing

def get_raw_text_data(input_dir):  
    fList=os.listdir(input_dir)
    # Create a list of file names with full path, eliminating subdirectory entries
    fList1 = [os.path.join(input_dir, f) for f in fList if os.path.isfile(os.path.join(input_dir, f))] 
    
    #max_files = 1000 #remove to get the entire corpus
    raw_corpus = ''
    for file in tqdm(fList1): #[0:max_files] 
        with codecs.open(file, 'r', 'utf-8') as f: 
                                        # 'latin_1') as f:
        #with open(file, encoding="utf8") as f:
            raw_corpus += ''.join(f.read())  
    corpus = re.sub(r"(\n|\r)+""|(@\w+)+", ' ', raw_corpus) #remove backslashes and words starting with @
    #corpus = re.sub(r"(as soon)+" "|(as well)+" "|(as if)+" "|(as quickly as possible)+" "|(as long)" "|(as usual)+" "|(such as)+" "|(as of yet)+" "|(as much)+" "|(as many)+" "|(like that)+" "|(like this)+" "|(like you)+" "|(like me)+" "|(like him)+" "|(like us)+" "|(like her)+" "|(anybody like)+" "|(anyone like)+", "", corpus)
    return corpus


# In[13]:

def tokenize_text(corpus, do_tokenize_words=True):
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    raw_sents = sent_tokenizer.tokenize(corpus) # Split text into sentences 
    if do_tokenize_words:
        result = [nltk.word_tokenize(sent) for sent in raw_sents]
    else: 
        result = raw_sents
    return result


# In[14]:

def extract_simile_candidates(sentences):
    comparisons = []
    for i_sent, sent in enumerate(sentences):
        if not 'like' in sent and not 'as' in sent: 
            continue 
        # exlude a single 'as', leaving in only '...as ... as...'
        if not 'like' in sent and len([word for word in sent if word=='as']) == 1: 
            continue
        pos_tagged = nltk.pos_tag(sent)
        for pair in pos_tagged:
            if pair[1] == 'IN' and (pair[0] == 'like' or pair[0] == 'as'):
                comparisons.append((i_sent, pos_tagged))
    return comparisons


# In[15]:

def filter_candidates(all_candidates, regex_filter):
    similes_candidates = []
    punkt = set(['.',',','-',':',';','!','?', '"', '\'', ')', '(', '%', '#', '[', ']', '@'])
    key_pos_tags = set(['NN', 'NNS', 'NNP']) #, 'VB', 'VBN', 'VBD', 'VBG']) # noun or verb
    for i_sent, tagged_sent in all_candidates:
        sent = [pair[0] for pair in tagged_sent]
        string = ' '.join(sent)
        if regex_filter and re.search(regex_filter, string):
            similes_candidates.append((i_sent, string, False))
            continue # flat out reject
            
        start_index = -1
        words_after = -1
        pos_tags = [pair[1] for pair in tagged_sent]
        if 'like' in sent:
            start_index = sent.index('like')
            #two_words_before_like = max(0, index_of_like - 4)
            words_after = min(len(sent), start_index + 6)
        elif 'as' in sent:
            start_index = sent.index('as')
            words_after = min(len(sent), start_index + 8)

        if start_index >= 0 and words_after > 0:
            index_of_punkt = 0
            for i in range(start_index, words_after): 
                if sent[i] in punkt: 
                    index_of_punkt = i
                    break 

            if index_of_punkt > start_index: 
                words_after = min(words_after, index_of_punkt)
            subphrase = sent[start_index:words_after]
            if not(not key_pos_tags.intersection(set(pos_tags[start_index:words_after]))): # make sure at least one key pos tag is present
                similes_candidates.append((i_sent, subphrase, True))
            else:
                similes_candidates.append((i_sent, subphrase, False))
    return similes_candidates


# In[16]:

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(['a', 'an', 'and', 'or', 'the',                   'his', 'her', 'my', 'your', 'their', 'our',                   'i', 'you', 'he', 'she', 'it', 'they', 'who', 'that', 'whose',                   'is', 'are', 'was', 'will', 'would',                   '.',',','-',':',';','!','?', '"', '\'', ')', '(', '%', '#', '[', ']', '@'])

def preprocess_words(wordlist): 
    wordset = set([])
    for word in wordlist: 
        word = word.lower()
        if word not in stop_words and len(word) > 1: 
            if word != 'as':
                word = lemmatizer.lemmatize(word)
            if word == 'like' or word == 'as': 
                word = '$cmpr'
            wordset.add(word)
    return wordset 
        
''' Precomputes a corpus (phrase search index) for a given list of phrases
    Optimization: create a data structure to speed up fuzzy matching as follows: 
    {'word' : [i, j, k, ...]}, where i, j, k are the row indices of all phrases containing 'word'. 
    For each new search query, we prefetch the relevant rows based in the words in that query, 
    prior to fuzzy matching. 
'''
def init_corpus_2match(wordlists): 
    lookup = {}
    all_wordsets = []
    for i_sent, words in wordlists: # for each phrase (word list)
        if not words:
            continue
        wordset = preprocess_words(words)
        if not(not wordset):
            i_row = len(all_wordsets)   
            all_wordsets.append(wordset)
            
            # update loookup index (dictionary of word to corpus row id)
            for word in wordset: 
                if word not in lookup: 
                    lookup[word] = [i_row]
                else: 
                    lookup[word].append(i_row)
    return (all_wordsets, lookup) 


''' Returns a list of matches for 'phrase' in 'wordsets' with 'min_similarity' 
'''
def fuzzy_match(words_in, search_index, min_similarity): 
    # init 
    phraset = preprocess_words(words_in)
    relevant_corpus_rows = search_index
    
    # prepare relevant subset of search index
    # the data could be in 2 different representations
    if isinstance(search_index, tuple): 
        corpus = search_index[0]
        lookup = search_index[1]

        # prefetch relevant corpus rows 
        relevant_corpus_row_ids = set([])
        for word in phraset: 
            if word not in lookup or word == '$cmpr':
                continue
            row_ids = lookup[word]
            for i in row_ids:
                relevant_corpus_row_ids.add(i)    
        relevant_corpus_rows = [corpus[i] for i in relevant_corpus_row_ids]  
    
    # todo: remove
    # print("input phrase: {}".format(phraset))
    # print("relevant phrase ids: {}".format(relevant_corpus_row_ids))
    
    
    # actually search
    nb_input = len(phraset)
    matches = []
    for wordset in relevant_corpus_rows: 
        intersect = phraset.intersection(wordset)
        n = len(intersect)
        if n/min(nb_input, len(wordset)) >= min_similarity and not(n < 2 and next(iter(intersect))=='$cmpr'): 
            #print(wordset)
            matches.append(wordset)
    return matches


# In[17]:

import operator

def train_similes_corpus(candidates):
    corpus_2match = init_corpus_2match(candidates)
    covered = set([])
    count_dict = {}
    for cand in candidates:
        if not cand: 
            continue
        phrase = ' '.join(cand)
        if phrase in covered:
            continue
        covered.add(phrase)
        result = fuzzy_match(cand, corpus_2match, 0.75)
        #print("result is {}".format(result))
        if result:
            count_dict[phrase] = len(result)
    
    sorted_counts = sorted(count_dict.items(), key=operator.itemgetter(1))
    sorted_counts.reverse()
    return count_dict, sorted_counts


# In[18]:

from tqdm import tqdm

def aggregate_similes_candidates(input_dir):  
    fList=os.listdir(input_dir)
    # Create a list of file names with full path, eliminating subdirectory entries
    fList1 = [os.path.join(input_dir, f) for f in fList if os.path.isfile(os.path.join(input_dir, f))] 
    
    #max_files = 1000 #remove to get the entire corpus
    all_candidates = []
    for i in tqdm(range(len(fList1))): #[0:max_files] 
        file = fList1[i]
        with codecs.open(file, 'r', 'utf-8') as f: 
                                        # 'latin_1') as f:
        #with open(file, encoding="utf8") as f:
            raw_text = ''.join(f.read()) 
            text = re.sub(r"(\n|\r)+""|(@\w+)+", ' ', raw_text) #remove backslashes and words starting with @
            sentences = tokenize_text(text)
            similes_candidates = extract_simile_candidates(sentences)
            similes_candidates = filter_candidates(similes_candidates, regex_filter)
            all_candidates.extend(similes_candidates)
    return all_candidates


# ## Extract simile candidates from raw text  

# In[19]:

from sklearn.externals import joblib

def train(input_dir, min_simile_freq): 
    similes_candidates = aggregate_similes_candidates(input_dir)
    count_dict, sorted_counts = train_similes_corpus(similes_candidates)

    # create actual corpus and save 
    top_similes_corpus = init_corpus_2match([(-1, item[0].split(' ')) for item in count_dict.items() if item[1] >= min_simile_freq])
    # save 
    joblib.dump(top_similes_corpus, "data/top_similes_corpus.pkl")
    return similes_candidates, sorted_counts


# ## ![](http://www.eventprophire.com/_images/products/large/danger_skull_sign_orange.jpg) Train (don't run it!)

# In[163]:


#similes_candidates, sorted_counts = train(train_dir_name, min_simile_freq)


# ## Test 

# In[22]:

def extract_tagged_simile_sents(sentences):
    simile_sents = []
    for sent in sentences: 
        if not re.search("<rule1s>", sent):
            continue
        sent = re.sub(r"(<rule1s>)|(</rule1s>)", "", sent)
        simile_sents.append(nltk.pos_tag(nltk.word_tokenize(sent))) 
    return simile_sents


def eval(sentence_text, similes_corpus, min_simile_freq): 
    sentences = tokenize_text(sentence_text, do_tokenize_words=True)
    sentences_orig = tokenize_text(sentence_text, do_tokenize_words=False)
        
    similes_candidates = extract_simile_candidates(sentences)
    similes_candidates = filter_candidates(similes_candidates, regex_filter)
    results = []
    for i_sent, cand, is_pred_simile in similes_candidates:
        if is_pred_simile:
            matches = fuzzy_match(cand, similes_corpus, 0.75)
            nb_matches = len(matches)
            if nb_matches >= min_simile_freq:
                is_pred_simile = True
            else:
                is_pred_simile = False
                 
        # LIKE vs. AS
        sub_index = 0
        sub_length = 0
        if 'like' in cand:
            sub_index = sentences_orig[i_sent].find('like')
            sub_length = 4
        elif 'as' in cand:
            sub_index = sentences_orig[i_sent].find('as')
            sub_length = 2
        global_index = sentence_text.find(sentences_orig[i_sent]) 
        results.append((is_pred_simile, # is simile? 
                        i_sent, # sentence index
                        global_index+sub_index, # index of first char of the sentence in the full text 
                        sub_length, # comparison string length
                        sentences_orig[i_sent], cand)) # simile
    return results



# Test last step: (pseudo-)"classification" of simile_candidates
def test(data_dir, similes_corpus, min_simile_freq): 
    raw_corpus = get_raw_text_data(data_dir)
    sentences = tokenize_text(raw_corpus, do_tokenize_words=False)
    true_simile_sents = extract_tagged_simile_sents(sentences)
    
    nb_true_pos = 0
    false_pos = []
    false_neg = []
    for true_simile_sent in true_simile_sents:
        # sent_words = [pair[0] for pair in tagged_sent]
        is_pred_simile = False
        sent = [pair[0] for pair in true_simile_sent] # remove POS tags 
        nb_matches = 0
        nb_true_pos += 1
        simile_candidates = filter_candidates([true_simile_sent], regex_filter)
        if not (not simile_candidates): 
            simile_candidate = simile_candidates[0]
            matches = fuzzy_match(simile_candidate[1], similes_corpus, 0.75)
            nb_matches = len(matches)
        
        if nb_matches >= min_simile_freq:
            is_pred_simile = True

        if not is_pred_simile:
            false_neg.append(' '.join(sent))
#         else 
#             print("'{}' is NOT a trite simile".format(cand))
#    precision = nb_true_pos / (nb_true_pos + len(false_pos))
#    recall = nb_true_pos / (nb_true_pos + len(false_neg))
#     print("=== Claddification Report ===")
#     print("Precision = {}".format(precision))
#     print("Recall = {}".format(recall))
#     print("=============================")
#     print ("-- False Negatives --")
#     for neg in false_neg:
#         print(neg)
        


# In[23]:

similes_corpus = joblib.load("data/top_similes_corpus.pkl")
# test(test_dir_name, similes_corpus, 1)


# In[24]:

# Misc unit tests 
#test_data = "Mysterious Mr. Fogg lives his life like a machine, really. In fact, he looks like a frog. That's the honest truth. He is as green as a frog."
#eval(test_data, similes_corpus, 20)


# In[74]:

def trite_similes(document):
    trite_similes = []
    raw_return = eval(document, similes_corpus, 20)
    for each in raw_return:
        if each[0] is True:
            trite_similes.append((each[2], each[3]))
    return trite_similes

        


# In[78]:

def nontrite_similes(document):
    nontrite_similes = []
    raw_return = eval(document, similes_corpus, 20)
    for each in raw_return:
        if each[0] is False:
            nontrite_similes.append((each[2], each[3]))
    return nontrite_similes
    


# In[75]:

#trite_similes(test_data)


# In[79]:

#nontrite_similes(test_data)


# In[ ]:



