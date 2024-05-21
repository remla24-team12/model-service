FROM python:3.11-slim

WORKDIR /app

COPY . /app

# Install git and Pipenv
RUN apt-get update && apt-get install -y git && pip install --no-cache-dir pipenv

# Install dependencies from Pipfile
RUN pipenv install --system --

# Define build arguments for environment variables
ARG CLIENT_ID
ARG CLIENT_SECRET

# Set environment variables
ENV CLIENT_ID=$CLIENT_ID
ENV CLIENT_SECRET=$CLIENT_SECRET

EXPOSE 5000

# Command to run the application
CMD ["python", "src/app.py"]
