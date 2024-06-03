from flask import Flask, request, jsonify
from flasgger import Swagger
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
import numpy as np
from keras.models import load_model
from lib_ml import preprocessing
from fetch_model import fetch_model
from dvc_commands import pull_from_dvc, push_to_dvc
import json
import os

app = Flask(__name__)
swagger = Swagger(app)
metrics = PrometheusMetrics(app)
CORS(app)


@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({"message": "The API is running"})


@app.route('/predict', methods=['POST'])
@metrics.counter('total_requests', 'Total number of requests')
@metrics.gauge('active_requests', 'Number of active requests')
@metrics.histogram('predict_request_duration_seconds', 'Histogram of request durations in seconds')
def predict():
    """
    Receives a URL, makes a phishing/valid prediction, returns result
    """
    model = load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model/model.keras'))

    data = request.get_json()
    input_data = preprocessing.process_new_input(data['input_data']['url'])

    y_pred = model.predict(input_data, batch_size=1000)
    y_pred_binary = (np.array(y_pred) <= 0.5).astype(int)

    return json.dumps({"result": y_pred.tolist()[0], "safe": y_pred_binary.tolist()[0]})


@app.route('/label', methods=['POST'])
def new_label():
    """
    Receives a URL and a user-provided label.
    Adds the label to the 'better_labels.txt' and pushes this to the remote using dvc. 
    """
    data = request.get_json()
    url = data.get('url')
    new_label = data.get('newLabel')

    # Ensure the required file is pulled from Google Drive using DVC
    pull_from_dvc()

    # Add new entry to the file
    file_path = 'data/better_labels.txt'
    with open(file_path, 'a') as file:
        file.write(f"{new_label}\t{url}\n")

    # Push updated file to DVC
    push_to_dvc()

    return jsonify({"message": "Data received", "url": url, "newLabel": new_label})


if __name__ == "__main__":
    fetch_model()

    app.run(host="0.0.0.0", port=5000, debug=True)
