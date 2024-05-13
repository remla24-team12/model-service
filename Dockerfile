# Base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install Git. You might need to update package lists before installing.
RUN apt-get update && apt-get install -y git

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["python", "src/app.py"]
