from bs4 import BeautifulSoup
from flask import Flask
from flask import request

import orwell

# Global variables
app = Flask(__name__)

with open('index.html', 'r') as f:
	html_doc = f.read()


@app.route("/")
def hello():
    return "Hello, world!"


@app.route("/marktext")
def tag_text():
	input_text = request.args.get('text', '')
	rules = request.args.get('rules', '').split(',')
	print(rules)
	text = orwell.marked_html_from_text(input_text, rules)	
	print(text)
	soup = BeautifulSoup(html_doc, 'html.parser')
	analyzed_text = soup.find(id='analyzed_text')
	analyzed_text.append(BeautifulSoup(text, 'html.parser'))

	return soup.prettify()

@app.route('/tada')
def tada():
	print('tada!')
	return('TADA!')

if __name__ == "__main__":
    app.run(debug=True)
