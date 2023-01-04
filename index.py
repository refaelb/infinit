from flask import Flask, request, render_template
import json
from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
print("Connection Successful")


app = Flask(__name__)
@app.route('/ui' , methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/login' , methods=['GET','POST'])
def login():
    mydb = client["app"]
    mycol = mydb["users"]
    json_data=json.loads(request.data)
    return read_from_db(json_data, mycol)

def read_from_db(json_data, mycol):
    mydoc = mycol.find().sort("user")
    list=[]
    for x in mydoc:
        output_user=x["user"]
        list.append(output_user)
    if json_data["user"] in list:
        output="login"
    else:
        output="logout"
    return(output)

@app.route('/createUser' , methods=['GET','POST'])
def create_user():
    json_data=json.loads(request.data)
    mydb = client["app"]
    mycol = mydb["users"]
    checker = read_from_db(json_data, mycol)
    if checker == ("login"):
        output = ("user alredy exists")
    else:
        output = write_to_db(json_data, mycol)
    return output

def write_to_db(json_data, mycol):
    myquery = { "user": json_data["user"] , "pass": json_data["pass"]}
    mydoc = mycol.insert_one(myquery)
    return "sucsess"
    
@app.route('/addHours' , methods=['GET','POST'])
def add_work_times():
    mydb = client["app"]
    json_data=json.loads(request.data)
    mycol=mydb[json_data["user"]]
    myquery = { "user": json_data["user"] , "count_hours": json_data["count_hours"]}
    mydoc = mycol.insert_one(myquery)
    return ("sucsess")

@app.route('/getHours' , methods=['GET','POST'])
def get_work_times():
    mydb = client["app"]
    json_data=json.loads(request.data)
    mycol=mydb[json_data["user"]]
    mydoc = mycol.find().sort(json_data["user"])
    count_hours=0
    for x in mydoc:
        count_hours=count_hours+int(x["count_hours"])
    print (count_hours)
    return ("your sum hours is :"+str(count_hours))