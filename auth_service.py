from flask import Flask, request, jsonify
import couchdb
from kafka import KafkaProducer
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# CouchDB connection
COUCHDB_SERVER = "http://admin:password@couchdb:5984/" # with nginx
# COUCHDB_SERVER = "http://admin:password@localhost:5984/" # without nginx

couch = couchdb.Server(COUCHDB_SERVER)

try:
    db = couch["jee_neet_db"]
except couchdb.http.ResourceNotFound:
    print("Database 'jee_neet_db' not found. Please create it in CouchDB.")
    exit(1)

# Kafka producer
producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
# producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password are required"}), 400

    # Query CouchDB using _find
    query = {
        "selector": {"email": email},
        "limit": 1
    }

    result = db.find(query)

    student = None
    for doc in result:
        student = doc
        break  # Only take the first match

    if student:
        if student["password"] == password:
            producer.send('login_events', {'email': email, 'action': 'login'})
            return jsonify({"status": "success", "username": student["name"]}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401
    else:
        return jsonify({"status": "error", "message": "Email not found"}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
