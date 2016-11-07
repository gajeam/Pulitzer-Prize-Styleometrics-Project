# Does Quality Journalism Follow Orwell's Rules of Writing?


A Natural Language Processing final project by Michelle Carney, Gabe Nicholas, Sayan Sanyal, and Natasha Timakova.


## Overview


In his 1946 essay ["Politics and the English Language,"](http://www.orwell.ru/library/essays/politics/english/e_polit/), George Orwell laid out [six rules](https://en.wikipedia.org/wiki/Politics_and_the_English_Language#Remedy_of_Six_Rules) for good expository writing. They are as follows:
* Never use a metaphor, simile, or other figure of speech which you are used to seeing in print.
* Never use a long word where a short one will do.
* If it is possible to cut a word out, always cut it out.
* Never use the passive where you can use the active.
* Never use a foreign phrase, a scientific word, or a jargon word if you can think of an everyday English equivalent.
* Break any of these rules sooner than say anything outright barbarous.


The overall objective of this project is to explore to what extent Pulitzer Prize winning articles conforms to these heuristics in comparison to other journalistic articles. To achieve this end, we will create a model that assigns quantitative values to each of the Orwell’s metrics. We will apply this model to three corpora: Reuters, the New York Times, and Pulitzer Prize winning articles.




## Methodology


Below are outlines of how we will measure each of Orwell's first five rules, who is in charge of implementing each rule, and the tools that they will use.


### Rule 1: Finding Common Metaphors and Similes


Similes are a type of comparisons, which, like metaphors, involve the comparison of one thing with another thing of a different kind and is used to make a description more emphatic or vivid. However, unlike metaphors, similes have specific recognizable patterns. Most often, patterns with words “like” or “as” are used. For example, “**as** brave **as** a lion,” “they were **like** two hummingbirds.” But *like* could be a verb, a noun or a preposition, depending on the context. Consider this example: “I feel *like* something is wrong.” How will we distinguish between all these uses?


#### Strategy


Our strategy is two-fold. First, we will extract all similes-like constructions from the target corpora. Second, we’ll use a list of trite similes to match it with the extracted ones and determine the percent of banal comparisons that the target corpus contains.
To train our deterministic classifier (“pattern matcher”), we’ll create a pattern for similes recognition and train it on The VU Amsterdam Metaphor Corpus. The corpus annotated for similes and metaphors and comprises 16 202 sentences and 236 423 tokens. In this corpus, similes are annotated with mFlag (metaphor flag) tags, among which tags “like” and “as” are the most popular. Unfortunately, the corpus has only 57 “like” and 28 “as”, so our training set will be quite limited. In order to not miss a simile, we will tune our classifier so it had low precision and high recall (that is, we will grab some irrelevant stuff, but won’t miss many relevant similes). Later, this imperfection will not matter, since we’ll be looking specifically for trite similes.


After training a pattern matcher on the Amsterdam Metaphor Corpus, we’ll apply it to two different corpora: our Pulitzer Prize winning texts and a Reuters corpus. In parallel, we’ll fetch the list of trite similes and create bags of words (one for each simile) out of it. These bags of words are then matched to our target text, as well as Reuters corpus for comparison. In order to spot in our journalist texts not only similes, repeated word-for-word from our trite similes list, but also their variations, we’ll tune our bag of words matching algorithm so that it accepts a 70-80% match too.


We would also like to incorporate the newly released [Metanet](https://metaphor.icsi.berkeley.edu/pub/en/index.php/Category:Metaphor) and see if there is a mapping of synsets to the larger metaphor categories. We may be able to see frequency of synsets and if they are being discussed literally within the text (by category or specific words signalling tangibility) or if it is a high probability of it being figurative.


#### Expected outcome


It is possible that some “likes” and “as” used not in the context of comparison will pass through our double filter of a pattern matcher and bag of words matcher, but it shouldn’t be a big percent. We expect to see fewer trite similes in Pulitzer Prize winning texts then in Reuters corpus, for the latter is not considered to be an epitome of a writing style. 


#### Resources


For this problem, we will us nltk. Additionally, we will be using WordNet, newly opened to the public [MetaNet](https://metaphor.icsi.berkeley.edu/pub/en/index.php/Category:Metaphor), and the Amsterdam Metaphor Corpus to train our figure of speech classifier.


#### Owners


Natasha will own the similes part of this section and Michelle will own the metaphors part, with cross-collaboration.




### Rule 2: Synonym Replaceability and Readability


#### Strategy


The problem of finding out how often articles use a long word where a short word will do can be broken into two sub-problems: finding which words can replace a given word and determining which of these words is more readable.


Let's look at the following example:


```
Alfonso wears glasses.
Bertha wears spectacles.
```


In this case, our program should recognize that the word `spectacles` has a simpler synonym that it could be replaced with. To find if each word is replaceable, the program will first look up the synsets for each of the words. In this case, it would return the following:


```
synset = [spectacles, specs, eyeglasses, glasses]
```


Next, we make sure that each of the synonyms can be used in the same context as the original word. We can do this by checking a corpus to see whether the dependency exists in a large corpus. In the case of checking the synonyms for `spectacles`, we would check that for each synonym, the relationship `dobj("wears", synonym)` exists somewhere in it.


To determine readability, we would combine term frequency and syllable calculations metrics. Syllable calculations are used in the [Flesch–Kincaid readability tests](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests), but this alone would miss out on the fact that in this case, `glasses` is a better word to use than `specs`.


We are still to determine which of nouns, verbs, and adjectives we will check for, although whichever we choose should not affect our general strategy much.




#### Resources


For this problem, we will use spaCy, since it offers very fast dependency detection and syllable counting. Additionally, this will pull in the Brown corpus as a baseline to check for existing dependencies.


#### Owners


Gabe will be the primary owner of this question. Natasha will also work on it.




### Rule 3: Finding Unnecessary Words


#### Strategy


The Purdue OWL style guide has a list of a couple dozen [often unnecessary words and phrases.](https://owl.english.purdue.edu/owl/resource/572/02/) To calculate unnecessary word usage, we will simply search for how frequently these terms occur.


#### Resources


We will use spaCy for this problem since it is somewhat faster for these basic functions than nltk.


#### Owners


Gabe will be the primary owner of this question.


### Rule 4: Passive vs Active Voice


#### Strategy


We shall use dependency parsers ([Stanford CoreNLP](http://stanfordnlp.github.io/CoreNLP), [SyntaxNet](https://www.tensorflow.org/versions/r0.9/tutorials/syntaxnet/index.html), SpaCy) to tag sentences with dependency attributes. Tags that specify passive voice indicators (nsubjpass (noun , csubjpass, auxpass) can be used to indicate whether a sentence is passive voice or not. We then assign the article a score based on the ratio of sentences that include a passive voice indicator within it. We cross validate using Google’s new SyntaxNet Dependency parser and use the average score as our final measure.


#### Resources


Stanford CoreNLP, SyntaxNet and SpaCy parsers all trained on the Universal Dependency dataset as published by their groups


#### Owners


Sayan will be the primary owner of this question


### Rule 5: Jargon Detection


#### Strategy


Our goal is to create our own corpus of jargon words in order to predict if other words are “jargony.”  We will look for compound words that are not in the dictionary, find common prefixes or suffixes, and not proper nouns. From this corpus, we will find their features using CountVectorizer or TDIDF and try to predict how much jargon is in each article. We are excited about this method since we are working on defining “jargon” - which is subjective.


#### Resources


We want to use resources like Wikipedia and dictionaries to create a corpus of words, a corpus for prefix and suffixes, and other articles to train our corpus.


#### Owners


The co-owners are Michelle, Natasha, and Sayan.




### Rule 6: The Whole Shebang 


Orwell's sixth rule is a meta one. It basically says to break any of these rules if you feel you ought to. In a sense, that is what the entirety of this project is asking—how often do good journalists break these rules? Our end product, a three-by-five matrix of scores for how each of our corpora conform to each of these rules, will essentially address this question.




### Scraping


A lot of the resources we are looking at - the text for the pulitzer prize winning articles, lists of metaphors and similes are on websites and formatted differently. We will use RoboBrowser in conjunction with BeautifulSoup to extract the text and create .csv datasets that can be resused by all components of our code.


## Grading


Since we have a project that breaks nicely into five parts, we can assign two points to each part. For each part, we believe that one point should be assigned for how much the end measurement calculates what it says it will. The other point should be determined by the clarity of logic with which the code for each section is presented.




## Week-By-Week Plan


*For 14 November 2016*
* Sayan will get a working web scraper (with help from Michelle and Gabe.)
* Sayan will get the STanford Dependency Parser up and running and connected to Python
* Natasha will have a fully compiled list of similes and will have the Amsterdam Metaphors list in a parsable format
* Michelle will scrape MetaNet and get it into a parseable format
* Gabe will compile the list of overused words and phrases and compile it into a parseable format
* Gabe will some basic dependency parsing working in spaCy


*For 21 November 2016*
* Sayan will finished active/passive sentence detection
* Michelle and Natasha will build the rules for jargon detection
* Gabe will finish the overused words and phrases detection
* Gabe will have gathered the Reuters and New York Times corpora


*For 30 November 2016*
* We will have functioning prototypes for detecting all five rules


*For 7 December 2016*
* Finishing bug fixes, optimizations, and documentation for all of the code
* Design and build a basic demo


