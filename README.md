# Detecting Orwell's Rules of Writing


A Natural Language Processing final project by Michelle Carney, Gabe Nicholas, Sayan Sanyal, and Natasha Timakova.


## Overview


In his 1946 essay ["Politics and the English Language,"](http://www.orwell.ru/library/essays/politics/english/e_polit/), George Orwell laid out [six rules](https://en.wikipedia.org/wiki/Politics_and_the_English_Language#Remedy_of_Six_Rules) for good expository writing. They are as follows:
* Never use a metaphor, simile, or other figure of speech which you are used to seeing in print.
* Never use a long word where a short one will do.
* If it is possible to cut a word out, always cut it out.
* Never use the passive where you can use the active.
* Never use a foreign phrase, a scientific word, or a jargon word if you can think of an everyday English equivalent.
* Break any of these rules sooner than say anything outright barbarous.

The overall objective of this project is to create a tool that highlights where pieces of text break these rules. To achieve this end, we will create a computational model that can detect each of these attributes. Our end product will provide examples as well as a comparison of how well our model does to human marked up text.



## Methodology


Below are outlines of how we will measure each of Orwell's first five rules, who is in charge of implementing each rule, and the tools that they will use.


### Rule 1: Finding Common Metaphors and Similes

According to the Oxford Dictionary of Phrase and Fable, metaphors are figures of speech in which "a word or phrase is applied to an object or action to which it is not literally applicable." One may refer to metaphors as to "hidden comparisons," except there is no connecting words like "as" or "like." Thus, in a phrase "she was just a turtle" about a slow person, "turtle" is a metaphor, while in a phrase "she was slow as a turtle" one can easily spot a simile. But not all metaphors are created equal. Some of them, like "I see what you are saying" are so well incorporated into our minds that it is hard for a human to distinguish them. We hypothesize, that the reason why these "low-level" metaphors are unditinguishable is that the semantic distance between metaphor ("see") and a word it replaes ("hear") is relatively small. Orwell, as we think, didn't mean these kind of metaphors. So we will focus on so called "high-level" metaphors, in which the semantic distance is greater, and the metaphor spans multiple domains (i.e., institution compared to an animal: "UC Berkeley roars above the rest - go bears!" or "Our country isn't soaring quite as high post-election"). We think, triteness is easier to detect in these types of metaphors which are those high-level metaphors that are overused.

Similes are a type of comparisons, which, like metaphors, involve the comparison of one thing with another thing of a different kind and is used to make a description more emphatic or vivid. However, unlike metaphors, similes have specific recognizable patterns. Most often, patterns with words “like” or “as” are used. For example, “**as** brave **as** a lion,” “they were **like** two hummingbirds.” But *like* could be a verb, a noun or a preposition, depending on the context. Consider this example: “I feel *like* something is wrong.” How will we distinguish between all these uses?


#### Strategy


Our strategy is two-fold. First, we will extract all similes-like constructions from the target corpora. Second, we’ll use a list of trite similes to match it with the extracted ones and determine the percent of banal comparisons that the target corpus contains.
To train our deterministic classifier (“pattern matcher”), we’ll create a pattern for similes recognition and train it on The VU Amsterdam Metaphor Corpus. The corpus annotated for similes and metaphors and comprises 16 202 sentences and 236 423 tokens. In this corpus, similes are annotated with mFlag (metaphor flag) tags, among which tags “like” and “as” are the most popular. Unfortunately, the corpus has only 57 “like” and 28 “as”, so our training set will be quite limited. In order to not miss a simile, we will tune our classifier so it had low precision and high recall (that is, we will grab some irrelevant stuff, but won’t miss many relevant similes). Later, this imperfection will not matter, since we’ll be looking specifically for trite similes.


After training a pattern matcher on the Amsterdam Metaphor Corpus, we will apply it to our text, fetch a list of trite similes, and create bags of words (one for each simile) out of it. These bags of words are then matched to our target text, as well as Reuters corpus for comparison. In order to spot in our journalist texts not only similes, repeated word-for-word from our trite similes list, but also their variations, we’ll tune our bag of words matching algorithm so that it accepts a 70-80% match too.


We would like to look into using [Metanet](https://metaphor.icsi.berkeley.edu/pub/en/index.php/Category:Metaphor) and the Amsterdam Corpus. We would first like to see if there is a co-occurance of high-level synsets (hypernyms) from the metaphors defined in these resources (i.e., government co-occurs with light at a high rate). We will look at the frequency distribution of the most commonly used metaphors to spot a metaphor "which we are used to seeing in print." We would then like to explore how to turn these high probability co-occurances into features to be used in vectorizers practiced in class. After we have a vectorizer based on these co-occurance features, we would like to try to run text with metaphors through it and pull out sentences that are detected as metaphors, and assess how our feature detection is performing, and where we can improve. We can improve the vectorizer or model based on what the output of the prediction is (i.e., high probability the sentence or paragraph has a metaphor), but we expect to find that it is easier to identify trite metaphors (as defined above) rather than high-level metaphors that span a text.

We expect to spot most similes and metaphors in the text, highlight them along with the probability that each of them is actualy a simile or metaphor, as well as assess their triteness for the user.

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


We shall use dependency parsers ([Stanford CoreNLP](http://stanfordnlp.github.io/CoreNLP), [SyntaxNet](https://www.tensorflow.org/versions/r0.9/tutorials/syntaxnet/index.html), SpaCy) to tag sentences with dependency attributes. Tags that specify passive voice indicators (nsubjpass (noun , csubjpass, auxpass) can be used to indicate whether a sentence is passive voice or not. We will then use this to highlight all of the passive voice sentences in a given article and assign the article a score based on the ratio of sentences that include a passive voice indicator within it. We cross validate using Google’s new SyntaxNet Dependency parser and use the average score as our final measure.


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


Orwell's sixth rule is a meta one. It basically says to break any of these rules if you feel you ought to. In a sense, that is what the entirety of this project is asking—how often do good journalists break these rules? Our end product will be a simple web interface that can take in a text and produce and output that both highlights where an article breaks each of the five rules and will provide a score for each article.




### Testing the Results

To test the results, all four members of the group will go through and mark up one large or two small texts and highlight where they break rules one, two, four, and five (our operational definition for rule three does not require human comparison.) The texts will from fiction, science, traditional news, and Orwell himself. Someone else in the group will also review each person's work to assure that the results are similar. Below is an example of how we will mark up the texts:

```
Jerry McBerry did not have any children of his own. His house was the <rule2>antithesis</rule2> of child-friendly. His house was as messy as Tom Sawyer's hair and his kitchen was no longer <rule1>as a pretty as a peacock.</rule1> But he did not mind. This was the way his house got when he worked long hours. And Jerry loved to work long hours. He had being running the <rule5>epidermal</rule5> health clinic for two years at this point and <rule1>it was his baby.<rule1> <rule4>He was totally consumed by the long hours because he knew nothing else.<rule4>
```



## Grading


Since we have a project that breaks nicely into five parts, we can assign two points to each part. For each part, we believe that one point should be assigned for how much the end measurement calculates what it says it will. The other point should be determined by the clarity of logic with which the code for each section is presented.




## Week-By-Week Plan


*For 14 November 2016*
* Sayan will get a working web scraper (with help from Michelle and Gabe.)
* Sayan will get the Stanford Dependency Parser up and running and connected to Python
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


