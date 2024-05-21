FROM python:3.11-slim

WORKDIR /app

COPY . /app
COPY ./src/secrets.json /app/src/secrets.json
COPY ./src/remla-team-12-2078257eb673.json /app/src/remla-team-12-2078257eb673.json

# Install git and Pipenv
RUN apt-get update && apt-get install -y git && pip install --no-cache-dir pipenv

# Install dependencies from Pipfile
RUN pipenv install --system

EXPOSE 5000

# Command to run the application
CMD ["python", "src/app.py"]
