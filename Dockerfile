FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y git

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Command to run the application
CMD ["python", "src/app.py"]
