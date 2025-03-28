# Distributed Computing Project

## Overview
This project is a distributed system designed for the popular JEE/NEET exams, whose wesbite during result declaration cannot handle multiple students' requests leading to downtime of the server.This handles authentication, user sign-up, and result processing using multiple microservices. It utilizes NGINX for load balancing, Apache Kafka for event handling, and Docker to containerize the services and couchdb to store all the students data.

## Features
- **Authentication Service**: Handles user login.
- **Signup Service**: Manages new user registrations.
- **Result Service**: Processes and retrieves results, with load balancing between two instances.
- **NGINX Load Balancing**: Distributes requests across multiple result service instances.
- **Kafka Event Handling**: Ensures smooth communication between services.
- **Docker Deployment**: Runs all services in isolated containers.


## Prerequisites
Ensure you have the following installed before proceeding:
- Docker & Docker Compose
- Python 3
- Apache Kafka
- NGINX
- CouchDB

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/dc_project.git
   cd dc_project
   ```

2. **Start Kafka**
   Ensure Kafka is running before starting the services.
   ```bash
   docker-compose up -d zookeeper kafka
   ```

3. **Build and Start the Services**
   ```bash
   docker-compose up --build
   ```

4. **Check Running Containers**
   ```bash
   docker ps
   ```
   You should see containers for NGINX, authentication, signup, and result services.

5. **Test the Setup**
   Use `curl` or Postman to send requests to the NGINX server.
   ```bash
   curl -X POST http://localhost:8080/results/get -H "Content-Type: application/json" -d '{"email": "user@example.com"}'
   ```

## Load Testing with Locust

1. **Start Locust**
   ```bash
   docker-compose up locust
   ```

2. **Access the Locust Web Interface**
   Open `http://localhost:8089` in a browser.

3. **Configure and Run Tests**
   - Set the number of users and spawn rate.
   - Start the test and monitor load distribution.

## Architecture
```
+-------------+       +-------------+       +-------------+
|   Client    | --->  |    NGINX    | --->  |  Result Svc |
+-------------+       +-------------+       +-------------+
                              |                 |
                              v                 v
                         Result Svc 1      Result Svc 2
```

## Notes
- Ensure ports in `docker-compose.yml` match your configuration.
- Kafka topics should be properly created before running services.
- Load balancing is configured in `nginx.conf`.

## Contributors
- Om Sable

## License
This project is licensed under MIT License.

