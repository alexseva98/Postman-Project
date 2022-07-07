from contextlib import nullcontext
from queue import Empty
from pymongo import MongoClient, cursor,collection
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import pymongo
import json
from bson import ObjectId
from bson.json_util import dumps
import uuid
import time

# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Choose database
db = client['DSNotes']

# Choose collections
notes = db['Notes']
users = db['Users']

# Initiate Flask App
app = Flask(__name__)

@app.route('/')

@app.route('/createUser', methods=['POST', 'GET'])
def create_user():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json') # WORKS(λαθος στοιχηση,πχ να λειπει καποιο κομμα κλπ)
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "username" in data or not "name" in data or not "surname" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json") # WORKS(λειπει καποιο πεδιο πχ email)

  
    # Έλεγχος δεδομένων email / password
    if not(users.find_one({"email":data["email"]})) and not(users.find_one({"username":data["username"]})) :
        new_user ={"email" : data['email'], "username" : data['username'],"name" : data['name'], "surname" : data['surname'],  "password" : data['password'], "category" : 'User'}
        users.insert_one(new_user)
        return Response(data['name']+" was added to the MongoDB", mimetype='application/json') # ΠΡΟΣΘΗΚΗ STATUS
 
    else:
        return Response("A user with the given email or username already exists", mimetype='application/json') # ΠΡΟΣΘΗΚΗ STATUS
    
# Login στο σύστημα
@app.route('/login', methods=['POST'])
def login():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json') # WORKS(λαθος στοιχηση,πχ να λειπει καποιο κομμα κλπ)
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json") # WORKS(λειπει καποιο πεδιο πχ email)

    # Έλεγχος δεδομένων email / password
    if users.find_one({"email":data["email"]}):
        global user_with_matching_email
        user_with_matching_email = users.find_one({"email" : data['email']})
        if user_with_matching_email['password'] == data['password'] :
            global user_email
            global user_category
            global user_username
            global user_name
            user_email = str(data['email'])
            user_name = str(user_with_matching_email['name'])
            user_category = str(user_with_matching_email['category'])
            if user_category != 'admin' and user_category != "newAdmin":
                user_username = str(user_with_matching_email['username'])
            else:
                user_username = "Admin"
                user_name = "Admin"
            return Response(f"{user_name} Logged in.",status=200 , mimetype='application/json')
        else:
            # Διαφορετικά, αν η αυθεντικοποίηση είναι ανεπιτυχής.
            return Response("Wrong email or password.", status=400 , mimetype='application/json') # ΠΡΟΣΘΗΚΗ STATUS
    else:
        # Διαφορετικά, αν η αυθεντικοποίηση είναι ανεπιτυχής.
        return Response("Wrong email or password.", status=400 , mimetype='application/json') # ΠΡΟΣΘΗΚΗ STATUS     

# Δημιουργια σημειωσης
@app.route('/insertNote', methods=['POST','GET'])
def insertNote():
    global user_category
    global user_note
    user_note = {}
    #Ελεγχος Χρηστη
    if user_category == "admin" or user_category == "newAdmin":
        return Response("Persmission Denied",status=401,mimetype="application/json")
    elif user_category == "User" :
        
        #ελεγχος Δεδομενων
        data = None 
        try:
            data = json.loads(request.data)
        except Exception as e:
            return Response("bad json content",status=500,mimetype='application/json') # WORKS(λαθος στοιχηση,πχ να λειπει καποιο κομμα κλπ)
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "title" in data or not "text" in data or not "keywords" in data :
            return Response("Information incomplete",status=500,mimetype="application/json") # WORKS(λειπει καποιο πεδιο πχ title)
        
        #Εισαγωγη Δεδομενων
        user_note ={"username":user_username,'title':data["title"], 'text':data["text"], 'keywords':data["keywords"],"time":time.asctime( time.localtime(time.time()) )}
        notes.insert_one(user_note)
        return Response("note added in notes.",status=201 , mimetype='application/json')

# Εμφανιση ολων των notes του χρηστη σε descending order
@app.route('/myNotes',methods=['GET'])
def myNotes():
        if user_category == "admin" or user_category == "newAdmin" :
            return Response("Admins Cannot access this menu",status=500,mimetype="application/json")
        users_notes = list(notes.find({"username" :user_with_matching_email['username']}).sort("time", pymongo.DESCENDING))
        if users_notes == 0 :
            return Response("You don't have any note saved.",status=404,mimetype="application/json")
        else:
            return Response(f"Your Notes: \n {users_notes}", status=200 , mimetype='application/json')
# Εμφανιση ολων των notes του χρηστη σε ascending order
@app.route('/myNotes/Ascending',methods=['GET'])
def myNotesAsc(): 
        if user_category == "admin" or  user_category == "newAdmin":
            return Response("Admins Cannot access this menu",status=500,mimetype="application/json")
        users_notes = list(notes.find({"username" :user_with_matching_email['username']}).sort("time", pymongo.ASCENDING))
        if users_notes == 0 :
            return Response("You don't have any note saved.",status=404,mimetype="application/json")
        else:
            return Response(f"Your Notes: \n {users_notes}", status=200 , mimetype='application/json')

# Διαγραφη σημειωσης
@app.route('/DeleteNote', methods=['POST','GET'])
def DeleteNote():

    # Ελεγχος Χρηστη
    global user_category
    if user_category == "admin" or user_category == "newAdmin":
        return Response("Persmission Denied",status=401,mimetype="application/json")
    elif user_category == "User" :

  # Ελεγχος Δεδομενων
        data = None 
        try:
            data = json.loads(request.data)
        except Exception as e:
            return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "title" in data:
            return Response("Information incomplete",status=500,mimetype="application/json")

        # Διαγραφη σημειωσης
        if notes.find_one({"username" :user_with_matching_email['username'],"title" :data['title']}):
                notes.delete_many({"username" :user_with_matching_email['username'],"title" :data["title"]})
                return Response(f"Your notes with title:{data['title']} have been deleted.",status=200 , mimetype='application/json')
        else:
             return Response("You don't have any note saved with that title",status=404,mimetype="application/json")
# Ενημερωση σημειωσης. ΔΕΝ ΛΕΙΤΟΥΡΓΕΙ
@app.route('/UpdateNote', methods=['POST','GET'])
def UpdateNote():

    # Ελεγχος Χρηστη
    global user_category
    if user_category == "admin" or user_category == "newAdmin":
        return Response("Persmission Denied",status=401,mimetype="application/json")
    elif user_category == "User" :

  # Ελεγχος Δεδομενων
        data = None 
        try:
            data = json.loads(request.data)
        except Exception as e:
            return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "title" in data:
            return Response("Information incomplete",status=500,mimetype="application/json")

        #Ενημερωση σημειωσης
        if notes.find_one({"username" :user_with_matching_email['username'],"title" :data['title']}):
            this_one = notes.find_one({"username" :user_with_matching_email['username'],"title" :data['title']})
            if "title" in data:
                notes.update(this_one,{"$set":{'title':data["title"]}})

            if "text" in data :
                notes.update(this_one,{"$set":{"text":data['text']}})    

            if "keywords" in data:
                notes.update(this_one,{"$set":{"keywords":data['keywords']}})

            if "time" in data:
                notes.update(this_one,{"$set":{"time":time.time()}})

            return Response("note updated.",status=200 , mimetype='application/json')
#Αναζητηση σημειωσης βαση τιτλου η λεξης κλειδιου       
@app.route('/SearchNote', methods=['POST','GET'])
def SearchNote():
 # Ελεγχος Χρηστη
    global user_category
    if user_category == "admin" or user_category == "newAdmin":
        return Response("Persmission Denied",status=401,mimetype="application/json")
    elif user_category == "User" :
    # Ελεγχος Δεδομενων
        data = None 
        try:
            data = json.loads(request.data)
        except Exception as e:
            return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "title" in data and not "keywords" in data:
            return Response("Information incomplete, please select a Title or a Keyword",status=500,mimetype="application/json")

        if "title" in data:
            users_notes_title = list(notes.find({"username" :user_with_matching_email['username'],"title" :data["title"]}))
            if len(users_notes_title) == 0:
                return Response("You don't have any note saved with that title",status=404,mimetype="application/json")
            else:
                return Response(f"Your Notes with the selected title\n {users_notes_title}", status=200 , mimetype='application/json')
 
        if "keywords" in data:
            users_notes_keywords = list(notes.find({"username" :user_with_matching_email['username'],"keywords" :data["keywords"]}).sort("time", pymongo.DESCENDING))
            if len(users_notes_keywords) == 0:
                return Response("You don't have any note saved with these keywords",status=404,mimetype="application/json")
            else:
                return Response(f"Your Notes with the selected keywords\n {users_notes_keywords}", status=200 , mimetype='application/json')

# Διαγραφη χρηστη απ τον ίδιο τον χρήστη
@app.route('/deleteThisUser', methods=['POST','GET'])
def deleteThisUser():
    global user_email
    global user_username
    notes.delete_many({"username" :user_with_matching_email['username']})
    users.delete_one({"username" :user_with_matching_email['username']})

    return Response("Your account and its notes have been deleted.",status=200 , mimetype='application/json') 

# CREATE ADMIN
@app.route('/createAdmin', methods=['POST', 'GET'])
def create_admin():

     # Ελεγχος Χρηστη
    global user_category
    if user_category == "User" :
        return Response("Persmission Denied",status=401,mimetype="application/json")
    elif user_category == "admin" or user_category == "newAdmin":

        # Request JSON data
        data = None 
        try:
            data = json.loads(request.data)
        except Exception as e:
            return Response("bad json content",status=500,mimetype='application/json') # WORKS(λαθος στοιχηση,πχ να λειπει καποιο κομμα κλπ)
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "email" in data or not "name" in data or not "password" in data:
            return Response("Information incomplete",status=500,mimetype="application/json") # WORKS(λειπει καποιο πεδιο πχ email)

    
        # Έλεγχος δεδομένων email / password
        if not(users.find_one({"email":data["email"]})) :
            new_user ={"email" : data['email'], "name" : data['name'], "password" : data['password'], "category" : 'newAdmin'}
            users.insert_one(new_user)
            return Response(data['name']+" was added to the MongoDB", mimetype='application/json') # ΠΡΟΣΘΗΚΗ STATUS
    
        else:
            return Response("A user with the given email already exists", mimetype='application/json') # ΠΡΟΣΘΗΚΗ STATUS


# Διαγραφη χρηστη απ τον admin         
@app.route('/deleteUser', methods=['POST','GET'])
def deleteUser():
     # Ελεγχος Χρηστη
    global user_category
    if user_category == "User" :
        return Response("Persmission Denied",status=401,mimetype="application/json")
    elif user_category == "admin" or user_category == "newAdmin":
     # ελεγχος Δεδομενων
         data = None 
         try:
            data = json.loads(request.data)
         except Exception as e:
            return Response("bad json content",status=500,mimetype='application/json')
         if data == None:
            return Response("bad request",status=500,mimetype='application/json')
         if not "username" in data:
             return Response("Information incomplete",status=500,mimetype="application/json") 

         if notes.find_one({"username" :data['username']}):
            notes.delete_many({"username" :data['username']})
            users.delete_one({"username": data['username']})
            return Response("account and its notes deleted.",status=200 , mimetype='application/json')
         else:
            return Response(f"User with username: {data['username']} doesnt exist",status=500,mimetype="application/json")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)