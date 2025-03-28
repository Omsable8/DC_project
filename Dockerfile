FROM python:3.10


COPY . /

RUN pip install --no-cache-dir -r requirements.txt 

EXPOSE 5000 5001 5002 5003

# Environment variable to specify which service to run
ARG SERVICE
ENV SERVICE=${SERVICE}

# Start the appropriate Python file based on the SERVICE argument
CMD ["sh", "-c", "python3 ${SERVICE}.py"]
