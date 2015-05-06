from flask import Flask
from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)
app.debug==True

@app.route('/')
def homepage():
	print "hi"
	return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)