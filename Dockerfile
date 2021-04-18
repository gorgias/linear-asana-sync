# Python image to use.
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# copy the requirements file used for dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

ENV FLASK_APP="src.app" FLASK_RUN_HOST="0.0.0.0" FLASK_RUN_PORT=5580

ENTRYPOINT ["flask", "run"]
