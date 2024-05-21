import os
import json
from flask import Flask, request
from flasgger import Swagger
from flask_cors import CORS
import dvc.api
import numpy as np
from keras.models import load_model
from lib_ml import preprocessing
import json

app = Flask(__name__)
swagger = Swagger(app)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Make a hardcoded prediction
    ---
    consumes:
      - application/json
    parameters:
      - name: input_data
        in: body
        description: URL to be classified.
        required: true
        schema:
          type: object
          properties:
            url:
              type: string
              example: https://www.example.org/bone.html
    responses:
      200:
        description: Some result
        schema:
          type: object
          properties:
            result:
              type: object
            safe:
              type: boolean

    """

    model = load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model/model.keras'))

    data = request.get_json()
    input_data = preprocessing.process_new_input(data['url'])

    y_pred = model.predict(input_data, batch_size=1000)
    y_pred_binary = (np.array(y_pred) <= 0.5).astype(int)

    print(y_pred_binary)

    return json.dumps({"result": y_pred.tolist()[0], "safe": y_pred_binary.tolist()[0]})

def fetch_model():
    """Fetch model and tokenizer from dvc registry"""

    artifact = dvc.api.artifacts_show(
        'phishing-detection',
        repo="https://github.com/remla24-team12/model-training.git"
    )

    fs = dvc.api.DVCFileSystem(
        url='https://github.com/remla24-team12/model-training.git',
        rev=artifact['rev'],
        gdrive_service_account_json_file_path='/app/remla-team-12-2078257eb673.json',
        gdrive_use_service_account = 'true'
    )

    fs.get_file(artifact['path'], os.path.join("model",os.path.basename(artifact['path'])))

if __name__ == "__main__":
    fetch_model()

    app.run(host="0.0.0.0", port=5000, debug=True)
