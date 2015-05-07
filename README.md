Jessica Fan jcf2167
Emily Chen ec2805

We collected ~1.8MB tweets about Obama and used MapReduce to classify the sentiment (either "positive" or "negative") of each tweet in our collection. Our mapper is implemented in python and we used AWS EMR's built in "aggregate" reducer. Each record processed by the mapper contains the text and timestamp of a tweet in our collection. The mapper assigns an intermediate key for a record based on both the timestamp and the sentiment classification of the associated tweet. The mapper is designed to emit intermediate keys such that reducers output the total count of positive and negative classications for each hourly time bucket, which gives us the desired form of data to visualize the trend of sentiment toward Obama over time.
