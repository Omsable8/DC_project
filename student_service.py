from flask import Flask, request, jsonify
import couchdb
import uuid  # To generate unique document IDs
import random

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# CouchDB connection
COUCHDB_URL = "http://admin:password@couchdb:5984/"
couch = couchdb.Server(COUCHDB_URL)
db = couch.create("jee_neet_db") if "jee_neet_db" not in couch else couch["jee_neet_db"]

@app.route('/students/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    try:

        # Check if roll number already exists
        for doc_id in db:
            if db[doc_id].get("email") == email:
                return jsonify({"status": "error", "message": "Roll number already exists"}), 400

        # Create a new document in CouchDB
        student_doc = {
            "_id": str(uuid.uuid4().hex),  # Generate a unique ID for the document
            "email": email,
            "name": name,
            "password": password,
            "results": {'Physics':random.randint(50,99),'Chemistry':random.randint(50,99),'Maths':random.randint(50,99)} 
        }

        db.save(student_doc)  # Correct way to insert a document
        return jsonify({"status": "success", "message": "Account created successfully"}), 201
    except Exception as e:
        print("Error: ",e)
        return jsonify({"status": "failed", "message": "Error occured while creaing account"}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
