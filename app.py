import boto
import json

from flask import Flask, render_template

app = Flask(__name__)
app.debug==True

job_bucket_name = 'hadoopjobcopy'
s3 = boto.connect_s3()
job_bucket = s3.get_bucket(job_bucket_name)
output_key_name = 'tsoutputbig'

@app.route('/')
def prep_stacked_area_data():
    num_pos = 0    
    num_neg = 0
    mr_output = []
    visualization_data = []
    for reducer_output in job_bucket.list():
        if reducer_output.name != '{}/'.format(output_key_name):
            lines = reducer_output.get_contents_as_string().rstrip().split('\n')
            for line in lines:
                if line.find('No match') > -1:
                    continue
                bin_data, count_data = line.split('\t')
                count = int(count_data)
                ts_data = bin_data.split(': ')[1]
                timestring, classification = ts_data.split('---')
                mr_output.append({'count': count, 'timestring':timestring, 'classification': classification})
    mr_output.sort(key=lambda x:x['timestring'])
    for datum in mr_output:
        classification = datum['classification']
        timestring = datum['timestring']
        count = datum['count']
        if classification == 'pos':
            num_pos += count
        if classification == 'neg':
            num_neg += count
        vis_datum = {'date': timestring, 'Positive': 100.0*num_pos/(num_pos+num_neg), 'Negative': 100.0*num_neg/(num_pos+num_neg)}
        visualization_data.append(vis_datum)
    date_to_record = visualization_data[0]['date']
    visualization_percentage_data = []
    for index, datum in enumerate(visualization_data):
        if datum['date'] != date_to_record:
            visualization_percentage_data.append(visualization_data[index-1])
            date_to_record = datum['date']
    visualization_percentage_data.append(visualization_data[-1])
    return render_template('index.html', results=json.dumps(visualization_percentage_data))

if __name__ == '__main__':
    app.run(debug=True)
