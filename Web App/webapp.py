from flask import Flask
from flask import request

import orwell

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/marktext")
def tag_text():
	text = request.args.get('text', '')
	print(text)
	text = orwell.marked_html_from_text(text)	
	print(text)
	return text

if __name__ == "__main__":
    app.run()
