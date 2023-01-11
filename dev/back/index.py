from flask import Flask, request, render_template
import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv('.env') 
# MONGO_URI = os.getenv('MONGO_URI')
MONGO_URI = os.environ.get('MONGO_URI')
print(MONGO_URI)
client = MongoClient(MONGO_URI)
# client = MongoClient("mongodb://"+MONGO_URI+":27017/app")

print("Connection Successful to mongo")


app = Flask(__name__)
@app.route('/ui' , methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/login' , methods=['GET','POST'])
def login():
    mydb = client["app"]
    mycol = mydb["users"]
    json_data=json.loads(request.data)
    return check_users_exists(json_data, mycol)

def check_users_exists(json_data: object, mycol: object):
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
    checker = check_users_exists(json_data, mycol)
    if checker == ("login"):
        output = ("user alredy exists")
    else:
        output = create_users(json_data, mycol)
    return output

def create_users(json_data: object, mycol: object):
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

@app.route('/getAll' , methods=['GET','POST'])
def get_all():
    mydb = client["app"]
    json_data=json.loads(request.data)
    mycol=mydb[json_data["user"]]
    mydoc = mycol.find().sort(json_data["user"])
    count_hours=[]
    for x in mydoc:
        count_hours.append(x)
        # count_hours=count_hours+int(x["count_hours"])
    print (count_hours)
    return ("your sum hours is :"+str(count_hours))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)