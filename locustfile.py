from locust import HttpUser, task, between
import json
import random

def generate_random_email():
    mails = ["a@gmail.com", "b@gmail.com", "c@gmail.com"]
    return random.choice(mails)
class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Simulates real users waiting between requests

    @task
    def login(self):
        payload = {
            "email": generate_random_email()
        }
        headers = {"Content-Type": "application/json"}

        # Send a login request to NGINX (which forwards it to Flask)
        response = self.client.post("/results/get", data=json.dumps(payload), headers=headers)

        # Print the response for debugging
        print(response.text)

# Run using: locust -f locustfile.py
