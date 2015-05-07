#!/usr/bin/python

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
import sys
import datetime
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

sys.stderr.write("Started mapper.\n");


def subj(subjLine):
    subjgen = subjLine.lower()
    subj1 = "obama"
    if subjgen.find(subj1) != -1:
        subject = subj1
        return subject
    else:
        subject = "No match"
        return subject


def main(argv):
    for line in sys.stdin:
        subjectFull = subj(line)
        if subjectFull == "No match":
            print "LongValueSum:" + " " + subjectFull + ": " + "\t" + "1"
        else:
            # define the intermediate key using time and sentiment classication
            text = line.rstrip()
            blob = TextBlob(text,analyzer=NaiveBayesAnalyzer())
            score = blob.sentiment.p_pos
            sentiment = 'pos' if score > 0.7 else 'neg'
            # ms since beginning of Unix Epoch
            timestamp = text.split(",")[1][5:]
            d = datetime.datetime.utcfromtimestamp(int(timestamp)/1000.0)
            time_map = {1: "01", 2:"02", 3:"03", 4:"04", 5:"05", 6:"06", 7:"07", 8:"08", 9:"09"}
            year = d.year
            month = d.month if d.month >= 10 else time_map[d.month]
            date = d.day if d.day >= 10 else time_map[d.day]
            hour = d.hour if d.hour >= 10 else time_map[d.hour]
            timebucket = "{yr}-{mon}-{dt}T{hr}".format(yr=year, mon=month, dt=date, hr=hour)
            intermediate_key = "{ts}---{cls}".format(ts=timebucket,cls=sentiment)
            sys.stderr.write("d.hour:{hr}\n".format(hr=d.hour))
            sys.stderr.write("timestamp:{ts} hour:{hr}.\n".format(ts=timestamp, hr=hour))
            # emit a tally for that time-sentiment bucket
            print "LongValueSum:" + " " + subjectFull + ": " + intermediate_key + "\t" + "1"


if __name__ == "__main__":
    main(sys.argv)
