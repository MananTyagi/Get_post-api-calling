from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import  ObjectId
import urllib.request
import requests
app= Flask(__name__)
try:
    mongo=pymongo.MongoClient(
        host="localhost",
        port= 27017,
        serverSelectionTimeoutMS=1000
    )
    db=mongo.company   #Company is name of database
    mongo.server_info()   #trigger exception id cannot connect to db
except:
    print("ERROR-cannot connect t0 db")
    
    
#read
@app.route("/getuser", methods=["GET"])
def get_some_user():
    try:
        data=list(db.users.find())
        for user in data:
            user["_id"]=str(user["_id"])
        return  Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        print(e)
        return  Response(
            response=json.dumps({"message":"Cannot read User"}),
            status=500,
            mimetype="application/json"
        )
        


#create 
@app.route('/users', methods=['POST'])
def create_user():
    try :
        user={"name":request.form['name'], "lastName":request.form['lastName']}
        dbresponse= db.users.insert_one(user)
        #for attribute in dir(dbresponse):
            #print(attribute)
        return  Response(
            response=json.dumps({"message":"User created successfully", "id":str(dbresponse.inserted_id)}),
            status=200,
            mimetype="application/json"
        )
        
    except Exception as e :
        print(e)
        
        
        
        
#update
@app.route("/users/<id>", methods=["PATCH"])
def update_user(id):
    try:
        dbResponse=db.users.update_one(
            {"_id":ObjectId(id)},
            {"$set": {"name":request.form["name"]}}   
        )
        if dbResponse.modified_count==1:
            return  Response(
                response=json.dumps({"message":"updated User"}),
                status=200,
                mimetype="application/json"
            )
            
        return  Response(
            response=json.dumps({"message":" Sorry! Nothing was updated"}),
            status=500,
            mimetype="application/json"
        )
    except Exception as e :
        print("Exception of update", e)
        return  Response(
            response=json.dumps({"message":" Sorry! Cannot update User"}),
            status=500,
            mimetype="application/json"
        )
        
        
        
#delete
@app.route("/user/<id>",methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse=db.users.delete_one(
            {"_id":ObjectId(id)}
        )
        if dbResponse.deleted_count==1:
            
            return  Response(
                response=json.dumps({"message":"User deleted"}),
                status=200,
                mimetype="application/json"
            )
        
        return  Response(
            response=json.dumps({"message":" Sorry! NO user was found in the database"}),
            status=500,
            mimetype="application/json"
        )
    except Exception as e :
        print("23456789987645678909876543456789987654345678909876543456789987654")
        print("Exception of delete", e)
        return  Response(
            response=json.dumps({"message":" Sorry! Cannot delete User"}),
            status=500,
            mimetype="application/json"
        )
#calling an api  
@app.route("/new", methods=["GET","POST"])
def api():
    pin_code=request.form["pin_code"]
    url="https://api.postalpincode.in/pincode/" + str(pin_code)
    url_req=urllib.request.urlopen(url)
    json_object=json.load(url_req)
    return  Response(
        response=json.dumps({"message":json_object}),
        status=200,
        mimetype="application/json"
    )
            
#calling an Post APi
@app.route("/post", methods=["POST", "GET"])
def dummy():
    try:
        name= request.form['name']
        job= request.form['job']
        api_url="https://reqres.in/api/users"
        data={
            "name": name,
            "job": job,
        }
        r = requests.post(url=api_url, json=data)
        return  Response(
            response=json.dumps({"message":r.text}),
            status=r.status_code,
            mimetype="application/json"
        )
    except Exception as e :
        print(e)
if __name__ == '__main__':
    app.run(port=80,debug=True)