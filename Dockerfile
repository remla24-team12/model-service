FROM python:3.11-slim

WORKDIR /app

COPY . /app

# Copy the service account key file into the Docker image
COPY remla-team-12-2078257eb673.json ./remla-team-12-2078257eb673.json


# Install git and Pipenv
RUN apt-get update && apt-get install -y git && pip install --no-cache-dir pipenv

# Install dependencies from Pipfile
RUN pipenv install --system --

EXPOSE 5000

# Command to run the application
CMD ["python", "src/app.py"]
