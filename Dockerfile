FROM python:3.11-slim

WORKDIR /app

COPY . /app

# Install git and Pipenv
RUN apt-get update && apt-get install -y git && pip install --no-cache-dir pipenv

# Install dependencies from Pipfile
RUN pipenv install --system --deploy

EXPOSE 5000

# Command to run the application
CMD ["python", "src/app.py"]
