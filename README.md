
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

Our work will explore to what extent Pulitzer Prize winning articles conforms to these heuristics in comparison to other journalistic articles. To achieve this end, we will create quantitative for all but the last of these rules and compare how three corpora score on them: the Reuters Corpus, the New York Times corpus, and a corpus we will create of Pulitzer Prize winning articles.


## Methodology

Below are outlines of how we will measure each of Orwell's first five rules, who is in charge of implementing each rule, and the tools that they will use.

### Rule 1: Finding Common Metaphors and Similes

Similes are a type of comparisons, which, like metaphors, involve the comparison of one thing with another thing of a different kind and is used to make a description more emphatic or vivid. However, unlike metaphors, similes have specific recognizable patterns. Most often, patterns with words “like” or “as” are used. For example, “**as** brave **as** a lion,” “they were **like** two hummingbirds.” But *like* could be a verb, a noun or a preposition, depending on the context. Consider this example: “I feel *like* something is wrong.” How will we distinguish between all these uses?

#### Strategy

Our strategy is two-fold. First, we will extract all similes-like constructions from the target corpora. Second, we’ll use a list of trite similes to match it with the extracted ones and determine the percent of banal comparisons that the target corpus contains.
To train our deterministic classifier (“pattern matcher”), we’ll create a pattern for similes recognition and train it on The VU Amsterdam Metaphor Corpus. The corpus annotated for similes and metaphors and comprises 16 202 sentences and 236 423 tokens. In this corpus, similes are annotated with mFlag (metaphor flag) tags, among which tags “like” and “as” are the most popular. Unfortunately, the corpus has only 57 “like” and 28 “as”, so our training set will be quite limited. In order to not miss a simile, we will tune our classifier so it had low precision and high recall (that is, we will grab some irrelevant stuff, but won’t miss many relevant similes). Later, this imperfection will not matter, since we’ll be looking specifically for trite similes.

After training a pattern matcher on the Amsterdam Metaphor Corpus, we’ll apply it to two different corpora: our Pulitzer Prize winning texts and a Reuters corpus. In parallel, we’ll fetch the list of trite similes and create bags of words (one for each simile) out of it. These bags of words are then matched to our target text, as well as Reuters corpus for comparison. In order to spot in our journalist texts not only similes, repeated word-for-word from our trite similes list, but also their variations, we’ll tune our bag of words matching algorithm so that it accepts a 70-80% match too.

#### Expected outcome

It is possible that some “likes” and “as” used not in the context of comparison will pass through our double filter of a pattern matcher and bag of words matcher, but it shouldn’t be a big percent. We expect to see fewer trite similes in Pulitzer Prize winning texts then in Reuters corpus, for the latter is not considered to be an epitome of a writing style. 

### Rule 2: Synonym Replaceability and Readability

#### Strategy

The problem of finding out how often articles use a long word where a short word will do can be broken into two sub-problems: finding which words can replace a given word and determing which of these words is more readable.

Let's look at the following example:

```
Alfonso wears glasses.
Bertha wears spectacles.
```

In this case, our program should recognize that the word `spectacles` has a simpler synonym that it could be replaced with. To find if each word is replaceable, the program will first look up the sysnets for each of the words. In this case, it would return the following:

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

*Insert discussion here*

### Rule 5: Jargon Detection

*Insert discussion here*

### Rule 6: The Whole Shebang 

Orwell's sixth rule is a meta one. It basically says to break any of these rules if you feel you ought to. In a sense, that is what the entirety of this project is asking—how often do good journalists break these rules? Our end product, a three-by-five matrix of scores for how each of our corpora conform to each of these rules, will essentially address this question.


### Scraping

*Insert discussion of how we will do it here.*

## Grading

Since we have a project that breaks nicely into five parts, we can assign two points to each part. For each part, we believe that one point should be assigned for how much the end measurement calculates what it says it will. The other point should be determined by the clarity of logic with which the code for each section is presented.


## Week-By-Week Plan

*We'll figure this out later*
