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

# Get list of classes for a student
@app.route('/student/<student_id>/classes', methods=['GET'])
def get_student_classes(student_id):

   cursor_students = students_coll.find()
   cursor_students_json = json.loads(dumps(cursor_students))
   student_name = cursor_students_json[0]
   
   cursor_grades = grades_coll.find()
   cursor_grades_1 = json.loads(dumps(cursor_grades))
   grades_df = json_normalize(cursor_grades_1)
   # print(grades_df.head())
   # print(student_id)
   grades_df = grades_df.loc[grades_df["student_id"] == int(student_id)]
   class_uniq = grades_df["class_id"].unique()
   grades_df = grades_df.reset_index(drop=True)
   # print(class_uniq)
   classes= []
   for class_ in class_uniq:
       temp= {}
       temp["class_id"]=str(class_)
       classes.append(temp)
   

   final_dict= {}
   final_dict["student_id"] = student_id
   final_dict["student_name"] = student_name["name"]
   final_dict["classes"] = classes
   final_result = []
   final_result.append(final_dict)
   
   return jsonify(final_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0')