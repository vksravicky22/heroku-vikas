from flask import Flask, render_template,request, jsonify
app = Flask(__name__)


import pymongo
import json
from bson.json_util import dumps
import pandas as pd
from pandas.io.json import json_normalize
import sys
import ast


# Connection to MongoDb
client = pymongo.MongoClient(
    'mongodb+srv://prodigal_be_test_01:prodigaltech@test-01-ateon.mongodb.net/sample_training')
db = client['sample_training']
grades_coll = db['grades']
students_coll = db['students']

student_marks_df=pd.DataFrame(columns=["student_id","total_marks","grade"])

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/students', methods=['GET'])
def get_students():

    
    # print(db.list_collection_names())
    # sys.exit()
    
    cursor = students_coll.find()
    cursor_1 = json.loads(dumps(cursor))
    student_df= json_normalize(cursor_1)
    student_df= student_df.reset_index(drop=True)
    student_df.rename(columns={"_id": "student_id",
                         "name": "student_name"}, inplace=True)
    student_json = student_df.to_dict('records')
    
    return jsonify(student_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0')