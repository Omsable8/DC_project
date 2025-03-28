from flask import Flask, request, jsonify
import couchdb
from flask_cors import CORS
from kafka import KafkaConsumer
import threading
import json

app = Flask(__name__)
CORS(app)

# CouchDB connection
# COUCHDB_SERVER = "http://admin:password@localhost:5984/"  # Ensure localhost is used (without nginx)
COUCHDB_SERVER = "http://admin:password@couchdb:5984/"  # Ensure localhost is used (with nginx)


try:
    couch = couchdb.Server(COUCHDB_SERVER)
    db = couch["jee_neet_db"]
except couchdb.http.ResourceNotFound:
    print("Database 'jee_neet_db' not found. Please create it in CouchDB.")
    exit(1)

# Kafka Consumer (Runs in Background)
def consume_login_events():
    try:
        consumer = KafkaConsumer(
            'login_events',
            bootstrap_servers='kafka:9092',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        for message in consumer:
            email = message.value.get('email')
            print(f"User {email} logged in. Fetching results...")
    except Exception as e:
        print(f"Kafka consumer error: {e}")

@app.route('/results/get', methods=['POST'])
def get_results():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({"status": "error", "message": "Email is required"}), 400

    # Query CouchDB using _find
    query = {
        "selector": {"email": email},
        "limit": 1
    }

    try:
        result = db.find(query)
        student = next(result, None)  # Fetch the first matching document
        if student and "results" in student:
            return jsonify({"status": "success", "results": student["results"]}), 200
        else:
            return jsonify({"status": "error", "message": f"Results not found"}), 405
    except Exception as e:
        return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

if __name__ == '__main__':
    threading.Thread(target=consume_login_events, daemon=True).start()  # Run Kafka consumer in background
    app.run(host='0.0.0.0', port=5002)
