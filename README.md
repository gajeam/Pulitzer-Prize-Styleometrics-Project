
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

*Insert discussion here*

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
