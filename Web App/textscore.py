import orwell
import sys
import copy


def export_marked_textfile(textfile, rules):
	try:
		f = open(textfile)
		text = f.read()
	except:
		print('Could not open textfile ' + textfile)
		exit(1)

	# Write the new file
	new_text_name = textfile.split('.txt')[0] + '_out.txt'
	newf = open(new_text_name, 'w')
	marked_text = orwell.text_marked_up_with_tags(text, rules)
	binary_file = convert_marked_to_binary(marked_text, copy.copy(rules))
	newf.write(marked_text)
	return binary_file


def update_marked_text_for_rule(textfile, rules):
	try:
		f = open(textfile)
		text = f.read()
	except:
		print('Could not open textfile ' + textfile)
		exit(1)

	for rule in orwell.ALL_RULES:
		print('Checking ' + rule + '...')
		if rule not in rules:
			start = orwell.start_tag_with_rule(rule, True)
			end = orwell.end_tag(rule)
			text = text.replace(start, '')
			text = text.replace(end, '')
		else:
			# Make sure the text exists somewhere in the rules
			findval = text.find(orwell.start_tag_with_rule(rule, True))
			if findval == -1:
				print('Could not find rule ' + rule + ' in ' + textfile)
				continue
	return convert_marked_to_binary(text, copy.copy(rules))

def convert_marked_to_binary(text, the_rules):
	if len(the_rules) == 0:
		print(text)
		return text

	rule = the_rules[0]
	start = orwell.start_tag_with_rule(rule, True)
	end = orwell.end_tag(rule)

	start_location = text.find(start)
	end_location = text.find(end)
	if start_location == -1 or end_location == -1:
		text = text.replace(start, '')
		text = text.replace(end, '')
		the_rules.pop(0)
		return convert_marked_to_binary(text, the_rules)
	start_location += len(start)
	text = text.replace(text[start_location:end_location], '~' * (end_location - start_location))

	text = text.replace(start, '', 1)
	text = text.replace(end, '', 1)
	return convert_marked_to_binary(text, the_rules)

def score_arrays(arr1, arr2):
	length = min(len(arr1), len(arr2))
	count = 0
	correct = 0
	for i in range(length):
		count += 1
		if arr1[i] == arr2[i]:
			correct += 1
	return correct/count

def main():
	marked_file = sys.argv[1]
	unmarked_file = sys.argv[2]
	rules = sys.argv[3].split(',')
	human_marked = update_marked_text_for_rule(marked_file, rules)
	computer_marked = export_marked_textfile(unmarked_file, rules)

	print('Human len: ' + str(len(human_marked)))
	print('Comp len: ' + str(len(computer_marked)))
	print('Correct: ' + str(score_arrays(human_marked, computer_marked)))

if __name__ == "__main__":
	main()