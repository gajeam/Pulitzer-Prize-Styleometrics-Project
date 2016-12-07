from bs4 import BeautifulSoup
from flask import Flask
from flask import request

import orwell

# Global variables
app = Flask(__name__)

with open('index.html', 'r') as f:
	html_doc = f.read()


def append_text_marked_with_rules(text, rules):
	text = orwell.marked_html_from_text(text, rules)	
	soup = BeautifulSoup(html_doc, 'html.parser')
	print(text)
	analyzed_text = soup.find(id='analyzed_text')
	analyzed_text.append(BeautifulSoup(text, 'html.parser'))
	return soup.prettify()


@app.route("/")
def hello():
    return "Hello, world!"


@app.route("/marktext")
def tag_text():
	print(request.args)
	input_text = request.args.get('text', '')
	rules = request.args.get('rules', '').split(',')
	return append_text_marked_with_rules(input_text, rules)


@app.route('/markfile')
def mark_file():
	filename = request.args.get('filename', '')
	filename = 'static/' + filename
	rules = request.args.get('rules', '').split(',')
	try:
		file = open(filename, 'r')
		file_text = file.read()
		print('Read file!')
	except:
		return('Cannot open file ' + filename)
	return append_text_marked_with_rules(file_text, rules)


if __name__ == "__main__":
    app.run()
