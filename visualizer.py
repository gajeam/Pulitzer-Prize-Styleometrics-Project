import collections
from spacy.en import English

print('Loading Rule 2...')
import Rule2.Rule2 as rule2
print('Loading Rule 3...')
import Rule3.Rule3 as rule3
print('Loading Rule 4...')
import Rule4.Rule4_Active_vs_Passive_Voice as rule4

## Constants
TAG_RULE1S = 'rule1s'
TAG_RULE1M = 'rule1m'
TAG_RULE2 = 'rule2'
TAG_RULE3 = 'rule3'
TAG_RULE4 = 'rule4'
TAG_RULE5 = 'rule5'

## Global Variables
ALL_RULES = [TAG_RULE1S, TAG_RULE1M, TAG_RULE2, TAG_RULE3, TAG_RULE4, TAG_RULE5]
print('Loading spacy model...')
nlp = English()

def build_tag_ranges_for_text(text, rules=ALL_RULES):
	all_tags = []
	for rule in rules:
		print('Calculating tags for ' + rule)
		if rule is TAG_RULE2:
			all_tags.extend([(rule, tag_range) for tag_range in rule2.rule2_ranges_in_text(text, nlp)])
		elif rule is TAG_RULE3:
			all_tags.extend([(rule, tag_range) for tag_range in rule3.rule3_ranges_in_text(text)])
		elif rule is TAG_RULE4:
			all_tags.extend([(rule, tag_range) for tag_range in rule4.rule4_ranges_in_text(text, nlp)])
	return all_tags


def text_marked_up_with_tags(text):
	marked_tags = build_tag_ranges_for_text(text)
	# Turn the tags into open and closed tags
	open_tag_indices = [(text_range[0], '<' + rule + '>') for (rule, text_range) in marked_tags]
	closed_tag_indices = [(text_range[0] + text_range[1], '</' + rule + '>') for (rule, text_range) in marked_tags]
	tag_dictionary = collections.defaultdict(list)
	for (index, tag) in  open_tag_indices + closed_tag_indices:
		tag_dictionary[index].append(tag)
    # Mark up the new text by putting the tags in at the character indices
	new_text = ''
	for i in range(len(text)):
	    index_tags = tag_dictionary[i]
	    for tag in index_tags:
	        new_text += tag
	    new_text += text[i]
	return new_text

print(text_marked_up_with_tags('He was eaten by a shark. And that is kind of interesting because sharks are tremendously cool.'))
