from flask import Flask, request, render_template, sessions
import json
from pymongo import MongoClient
import os 
from dotenv import load_dotenv

load_dotenv() 
MONGO_URI = (os.environ['MONGO_URI'])
print(MONGO_URI)
client = MongoClient(MONGO_URI)
print("Connection Successful to mongo")

mydb = client["app"]
mycol = mydb["users"]

app = Flask(__name__)
@app.route('/ui' , methods=['GET','POST'])
def home():
    return render_template('index.html')
def validate_params(json_data, path):
    if path=="Hours":
        try:
            user=json_data["user"] 
            count_hours=json_data["count_hours"] 
            return ("200")
        except:
            return ("400")
    elif path=="login":
        try:
            user=json_data["user"] 
            password=json_data["password"]
            print(user, password) 
            return ("200")
        except:
            return ("400")
    elif path =="getAll":
        try:
            user=json_data["user"] 
            return ("200")
        except:
            return ("400")
        
@app.route('/login' , methods=['GET','POST'])
def login(*args, **kwargs):
    global mycol
    json_data=json.loads(request.data)
    status=validate_params(json_data, path="login")
    if status==("200"):
        print ("ok")
        return check_users_exists(json_data, mycol)
    else:
        return ("the request is requierd!")
    
def check_users_exists(json_data: object, mycol: object):
    try:
        mydoc = mycol.find().sort("user")
        list=[]
        for x in mydoc:
            print (x)
            output_user=x["user"]
            list.append(output_user)
        if json_data["user"] in list:
            return("login")
        else:
            return("Unauthenticated")
    except:
        print ("hi")
        return "503"

@app.route('/createUser' , methods=['GET','POST'])
def create_user(*args, **kwargs):
    global mycol
    json_data=json.loads(request.data)
    print (json_data)
    validate = validate_params(json_data, path="login")
    if validate == ("400"):
        print ("parameters...")
        return("Incorrect parameters")
    else:
        status = check_users_exists(json_data, mycol)
        print (status)
    if status == ("login"):
        return ("409 user exists! ")
    else:
        return create_users(json_data, mycol)

def create_users(json_data: object, mycol: object):
    try:
        myquery = { "user": json_data["user"] , "pass": json_data["pass"]}
        mydoc = mycol.insert_one(myquery)
        return "201 sucsess"
    except:
        return "503"

@app.route('/addHours' , methods=['GET','POST'])
def add_work_times(*args, **kwargs):
    global mydb
    json_data=json.loads(request.data)
    status = validate_params(json_data, path="Hours")
    if status == "200":
        try:
            mycol=mydb[json_data["user"]]
            myquery = { "user": json_data["user"] , "count_hours": json_data["count_hours"]}
            mydoc = mycol.insert_one(myquery)
            return ("201 sucsess")
        except:
            return "503"
    else:
        return("Incorrect parameters")
        

@app.route('/getHours' , methods=['GET','POST'])
def get_work_times(*args, **kwargs):
    global mydb
    json_data=json.loads(request.data)
    status = validate_params(json_data, path="Hours")
    if status=="200":
        try:
            mycol=mydb[json_data["user"]]
            mydoc = mycol.find().sort(json_data["user"])
            count_hours=0
            for x in mydoc:
                count_hours=count_hours+int(x["count_hours"])
            print (count_hours)
            return ("your sum hours is :"+str(count_hours))
        except:
            return "503"
    else:
        return "Incorrect parameters"

@app.route('/getAll' , methods=['GET','POST'])
def get_all(mydb):
    json_data=json.loads(request.data)
    status=validate_params(json_data, path="getAll")
    if status=="200":
        try:
            mycol=mydb[json_data["user"]]
            mydoc = mycol.find().sort(json_data["user"])
            count_hours=[]
            for x in mydoc:
                count_hours.append(x)
            print (count_hours)
            return ("your sum hours is :"+str(count_hours))
        except:
            return "503"
    else:
        return "Incorrect parameters"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)