from flask import Flask
from flask import Flask, render_template
import mysql.connector



app = Flask(__name__)
app.debug==True

config = {
  'user': 'jessicafan',
  'password': 'jessicafan',
  'host': 'cloud.c1xwtu16srrr.us-east-1.rds.amazonaws.com',
  'database': 'cloud',
  'raise_on_warnings': True,
}

@app.route('/')
def homepage():
	totalScore = 0
	numPos = 0
	numNeg = 0
	print "hi"
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
    query = "select time,sentiment,score from hadooptweets h order by h.time"
	cursor.execute(query)
	for (time, sentiment, score) in cursor:
		totalScore += score
		if score > .7:
			numPos +=1
		else:
			numNeg +=1



	return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)