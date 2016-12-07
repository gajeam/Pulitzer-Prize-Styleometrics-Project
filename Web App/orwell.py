import collections
from spacy.en import English

print('Loading Rule 1s...')
import rule1 as rule1s
print('Loading Rule 1m...')
import rule1m
print('Loading Rule 2...')
import rule2
print('Loading Rule 3...')
import rule3
print('Loading Rule 4...')
import rule4
print('Loading Rule 5...')
import rule5
print('Finished loading rules ;)\n')

## Constants
TAG_RULE1S_TRITE = 'rule1s'
TAG_RULE1S_NOT_TRITE = 'rule1s_not_trite'
TAG_RULE1M = 'rule1m'
TAG_RULE2 = 'rule2'
TAG_RULE3 = 'rule3'
TAG_RULE4 = 'rule4'
TAG_RULE5 = 'rule5'

## Global Variables
ALL_RULES = [TAG_RULE1S_TRITE, TAG_RULE1S_NOT_TRITE, TAG_RULE1M, TAG_RULE2, TAG_RULE3, TAG_RULE4, TAG_RULE5]
print('Loading spacy model...')
nlp = English()

def build_tag_ranges_for_text(text, rules):
	all_tags = []
	for rule in rules:
		print('Calculating tags for ' + rule)
		if rule == TAG_RULE1S_TRITE:
			all_tags.extend([(rule, tag_range) for tag_range in rule1s.trite_similes(text)])
		if rule == TAG_RULE1S_NOT_TRITE:
			all_tags.extend([(rule, tag_range) for tag_range in rule1s.nontrite_similes(text)])
		if rule == TAG_RULE1M:
			all_tags.extend([(rule, tag_range) for tag_range in rule1m.rule1m_ranges_in_text(text)])
		if rule == TAG_RULE2:
			all_tags.extend([(rule, tag_range) for tag_range in rule2.rule2_ranges_in_text(text, nlp)])
		if rule == TAG_RULE3:
			all_tags.extend([(rule, tag_range) for tag_range in rule3.rule3_ranges_in_text(text)])
		if rule == TAG_RULE4:
			all_tags.extend([(rule, tag_range) for tag_range in rule4.rule4_ranges_in_text(text, nlp)])
		if rule == TAG_RULE5:
			all_tags.extend([(rule, tag_range) for tag_range in rule5.rule5_ranges_in_text(text)])

	return all_tags


def text_marked_up_with_tags(text, rules):
	print(rules)
	marked_tags = build_tag_ranges_for_text(text, rules)
	# Turn the tags into open and closed tags
	open_tag_indices = [(text_range[0], start_tag_with_rule(rule)) for (rule, text_range) in marked_tags]
	closed_tag_indices = [(text_range[0] + text_range[1], end_tag()) for (rule, text_range) in marked_tags]
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


def start_tag_with_rule(rule, debug=False):
	if debug == True:
		return '(' + rule + ')'
	return '<span class = "' + rule + '">'
def end_tag():
	return '</span>'

def marked_html_from_text(text, rules=ALL_RULES):
	# rules = [TAG_RULE4]
	marked_text = text_marked_up_with_tags(text, rules)
	marked_text = '<p>' + marked_text + '</p>'
	marked_text = marked_text.replace('\n', '</p><p>')
	return marked_text

# print(marked_html_from_text('He was eaten by a shark. And that is kind of interesting because sharks are tremendously cool.', [TAG_RULE4]))
