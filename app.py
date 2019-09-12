import flask
from flask import request, jsonify
from flask import Flask, render_template


import pymongo
import json
from bson.json_util import dumps
import pandas as pd
from pandas.io.json import json_normalize
import sys
import ast



app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Connection to MongoDb
client = pymongo.MongoClient(
    'mongodb+srv://prodigal_be_test_01:prodigaltech@test-01-ateon.mongodb.net/sample_training')
db = client['sample_training']
grades_coll = db['grades']
students_coll = db['students']

student_marks_df=pd.DataFrame(columns=["student_id","total_marks","grade"])


def student_marks(student_id, total_marks):
    len_ = len(student_marks_df)
    student_marks_df.loc[len_, "student_id"] = student_id
    student_marks_df.loc[len_, "total_marks"] = total_marks
    return None


@app.route('/', methods=['GET'])
def hello_():
   return render_template('hello.html')

# Get all students
@app.route('/students', methods=['GET'])
def get_students():

    
    print(db.list_collection_names())
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
    print(grades_df.head())
    print(student_id)
    grades_df = grades_df.loc[grades_df["student_id"] == int(student_id)]
    class_uniq = grades_df["class_id"].unique()
    grades_df = grades_df.reset_index(drop=True)
    print(class_uniq)
    classes= []
    for class_ in class_uniq:
        temp= {}
        temp["class_id"]=str(class_)
        classes.append(temp)
    
    print(classes)
    # student_name = student_df.loc[student_df["_id"] == student_id,"name"].iloc[0]

    final_dict= {}
    final_dict["student_id"] = student_id
    final_dict["student_name"] = student_name["name"]
    final_dict["classes"] = classes
    final_result = []
    final_result.append(final_dict)
    
    return jsonify(final_result)


# Get aggregate performance in each class for a student
@app.route('/student/<student_id>/performance', methods=['GET'])
def get_aggregate_performance(student_id):

    cursor_students = students_coll.find()
    cursor_students_json = json.loads(dumps(cursor_students))
    student_name = cursor_students_json[0]

    cursor_grades = grades_coll.find()
    cursor_grades_1 = json.loads(dumps(cursor_grades))
    grades_df = json_normalize(cursor_grades_1)
    print(grades_df.head())
    print(student_id)
    grades_df = grades_df.loc[grades_df["student_id"] == int(student_id)]
    class_uniq = grades_df["class_id"].unique()
    grades_df = grades_df.reset_index(drop=True)
    print(class_uniq)
    classes = []
    for class_ in class_uniq:
        scores= grades_df.loc[grades_df["class_id"]==class_,"scores"].iloc[0]
        print(scores)
        total_marks=0
        for type_ in scores:
            total_marks += type_["score"]
        print(total_marks)
        # sys.exit()
        temp = {}
        temp["class_id"] = str(class_)
        temp["total_marks"] = str(int(total_marks))
        classes.append(temp)

    print(classes)
    # student_name = student_df.loc[student_df["_id"] == student_id,"name"].iloc[0]

    final_dict = {}
    final_dict["student_id"] = student_id
    final_dict["student_name"] = student_name["name"]
    final_dict["classes"] = classes
    final_result = []
    final_result.append(final_dict)
    
    return jsonify(final_result)

# Get all classes
@app.route('/classes', methods=['GET'])
def get_classes():

    print(db.list_collection_names())
    # sys.exit()

    cursor = grades_coll.find()
    cursor_1 = json.loads(dumps(cursor))
    grades_df = json_normalize(cursor_1)
    class_uniq = grades_df["class_id"].unique()
    grades_df = grades_df.reset_index(drop=True)
    print(class_uniq)
    classes=[]
    for class_ in class_uniq:
        temp = {}
        temp["class_id"] = str(class_)
        classes.append(temp)
    
    return jsonify(classes)

# Get list of students taking a course
@app.route('/class/<class_id>/students', methods=['GET'])
def get_class_students(class_id):
    cursor_students = students_coll.find()
    cursor_students_json = json.loads(dumps(cursor_students))
    

    cursor_grades = grades_coll.find()
    cursor_grades_1 = json.loads(dumps(cursor_grades))
    grades_df = json_normalize(cursor_grades_1)
    print(grades_df.head())
    print(class_id)
    grades_df = grades_df.loc[grades_df["class_id"] == int(class_id)]
    student_uniq = grades_df["student_id"].unique()
    # grades_df = grades_df.reset_index(drop=True)
    print(student_uniq)
    students = []
    for student_ in student_uniq:
        student_name = cursor_students_json[student_]
        temp = {}
        temp["student_id"] = str(student_)
        temp["student_name"] = str(student_name["name"])
        students.append(temp)

    print(students)
    # student_name = student_df.loc[student_df["_id"] == student_id,"name"].iloc[0]

    final_dict = {}
    final_dict["class_id"] = class_id
    final_dict["students"] = students
    final_result = []
    final_result.append(final_dict)

    return jsonify(final_result)


# Get aggregate performance of each student taking a course
@app.route('/class/<class_id>/performance', methods=['GET'])
def get_class_students_performance(class_id):
    # print(db.list_collection_names())
    cursor_students = students_coll.find()
    cursor_students_json = json.loads(dumps(cursor_students))

    cursor_grades = grades_coll.find()
    cursor_grades_1 = json.loads(dumps(cursor_grades))
    grades_df = json_normalize(cursor_grades_1)
    print(grades_df.head())
    print(class_id)
    grades_df = grades_df.loc[grades_df["class_id"] == int(class_id)]
    student_uniq = grades_df["student_id"].unique()
    # grades_df = grades_df.reset_index(drop=True)
    print(student_uniq)
    students = []
    for student_ in student_uniq:
        student_name = cursor_students_json[student_]
        scores = grades_df.loc[grades_df["student_id"] == int(
            student_), "scores"].iloc[0]
        print(scores)
        total_marks = 0
        for type_ in scores:
            total_marks += type_["score"]
        print(type(total_marks))

        temp = {}
        temp["student_id"] = str(student_)
        temp["student_name"] = str(student_name["name"])
        temp["total_marks"] = str(int(total_marks))
        students.append(temp)

    print(students)
    # student_name = student_df.loc[student_df["_id"] == student_id,"name"].iloc[0]

    final_dict = {}
    final_dict["class_id"] = class_id
    final_dict["students"] = students
    final_result = []
    final_result.append(final_dict)
    return jsonify(final_result)


# Get grades for a particular course
@app.route('/class/<class_id>/final-grade-sheet', methods=['GET'])
def get_class_students_final_grade_sheet(class_id):
    global student_marks_df
    # print(db.list_collection_names())
    cursor_students = students_coll.find()
    cursor_students_json = json.loads(dumps(cursor_students))

    cursor_grades = grades_coll.find()
    cursor_grades_1 = json.loads(dumps(cursor_grades))
    grades_df = json_normalize(cursor_grades_1)
    print(grades_df.head())
    print(class_id)
    grades_df = grades_df.loc[grades_df["class_id"] == int(class_id)]
    student_uniq = grades_df["student_id"].unique()
    # grades_df = grades_df.reset_index(drop=True)
    print(student_uniq)
    students = []
    for student_ in student_uniq:
        student_name = cursor_students_json[student_]
        scores = grades_df.loc[grades_df["student_id"] == int(
            student_), "scores"].iloc[0]
        print(scores)
        details=[]
        total_marks = 0
        for type_ in scores:
            _temp={}

            _temp["type"] = str(type_["type"])
            # _temp["type"] = str(type_["score"])
            details.append(_temp)
            total_marks += type_["score"]
        print(total_marks)
        temp_1={}
        temp_1["total_marks"] = int(total_marks)
        details.append(temp_1)

        temp = {}
        temp["student_id"] = str(student_)
        temp["student_name"] = str(student_name["name"])
        temp["details"] = details
        temp["grade"]=str(1)
        students.append(temp)
        student_marks(student_, total_marks)

    print(students)
    # student_name = student_df.loc[student_df["_id"] == student_id,"name"].iloc[0]
    student_marks_df.sort_values(by="total_marks", ascending=False, inplace=True)
    student_marks_df = student_marks_df.reset_index(drop=True)
    print(len(student_marks_df))
    length_ = len(student_marks_df)
    a_= length_*(1/12)
    a_=int(a_)
    ranges_a = list(range(0, a_))
    b_ = (length_-a_)*(1/6)
    b_ = int(b_)
    ranges_b = list(range(a_, a_+b_))
    c_ = (length_-(a_+b_))*(1/4)
    c_ = int(c_)
    ranges_c = list(range(a_+b_, a_+b_+c_))
    
    ranges_d = list(range(a_+b_+c_, length_))

    student_marks_df.loc[student_marks_df.index.isin(ranges_a), 'grade'] = 'A'
    student_marks_df.loc[student_marks_df.index.isin(ranges_b), 'grade'] = 'B'
    student_marks_df.loc[student_marks_df.index.isin(ranges_c), 'grade'] = 'C'
    student_marks_df.loc[student_marks_df.index.isin(ranges_d), 'grade'] = 'D'
    print(student_marks_df)

    for student_ in students:
        st_id= student_["student_id"]
        grade_= student_marks_df.loc[student_marks_df["student_id"]
                             == int(st_id), "grade"].iloc[0]
        student_["grade"] = grade_

    final_result= []
    final_dict = {}
    final_dict["class_id"] = class_id
    final_dict["students"] = students
    # final_dict["grade"] = students
    final_result.append(final_dict)
    # final_json = json.dumps(final_result)
    return jsonify(final_result)


# Get grades for a particular course
@app.route('/class/<class_id>/student/<student_id>', methods=['GET'])
def get_class_student_final_grade_sheet(class_id, student_id):
    global student_marks_df
    # print(db.list_collection_names())
    cursor_students = students_coll.find()
    cursor_students_json = json.loads(dumps(cursor_students))

    cursor_grades = grades_coll.find()
    cursor_grades_1 = json.loads(dumps(cursor_grades))
    grades_df = json_normalize(cursor_grades_1)
    print(grades_df.head())
    print(class_id)
    grades_df = grades_df.loc[grades_df["class_id"] == int(class_id)]
    student_class_df = grades_df[grades_df["student_id"] == int(student_id)]
    student_class_df = student_class_df.reset_index(drop=True)
  
  
    marks= []
    for marks_ in range(4):
        marks_temp = {}
        # print(student_class_df.loc[0, "scores"])
        list_temp= student_class_df.loc[0, "scores"]
        print(list_temp)
        # sys.exit()
        marks_temp["type"] = list_temp[marks_]["type"]
        marks_temp["marks"] = int(list_temp[marks_]["score"])
        marks.append(marks_temp)
    student_name = cursor_students_json[int(student_id)]
    final_result = []
    final_dict = {}
    final_dict["class_id"] = int(class_id)
    final_dict["student_id"] = int(student_id)
    final_dict["student_name"] = student_name["name"]
    final_dict["marks"] = marks
    # final_dict["grade"] = students
    final_result.append(final_dict)
    # final_json = json.dumps(final_result)
    return jsonify(final_result)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
