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
import os

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
    input_data = preprocessing.process_new_input(data['input_data']['url'])

    y_pred = model.predict(input_data, batch_size=1000)
    y_pred_binary = (np.array(y_pred) <= 0.5).astype(int)

    print(y_pred_binary)

    return json.dumps({"result": y_pred.tolist()[0], "safe": y_pred_binary.tolist()[0]})

def fetch_model():
    """Fetch model and tokenizer from dvc registry"""

    # Get the absolute path of the directory containing the current script
    # script_dir = os.path.dirname(os.path.abspath(__file__))

    # Change the current working directory to the directory of the current script
    # os.chdir(script_dir)

    print("Current Working Directory:", os.getcwd())

    directory_contents = os.listdir('.')

    # Print each item in the directory
    for item in directory_contents:
        print(item)


    secrets = load_secrets()

    
    artifact = dvc.api.artifacts_show(
        'phishing-detection',
        repo="https://github.com/remla24-team12/model-training.git"
    )

    config = {
        'remote': {
            'gdrive': {
                'gdrive_service_account_json_file_path': './src/remla-team-12-2078257eb673.json',
                'gdrive_client_id': secrets["CLIENT_ID"],
                'gdrive_client_secret': secrets["CLIENT_SECRET"],
                'gdrive_use_service_account': True  # Use True as a boolean, not a string
            }
        }
    }

    fs = dvc.api.DVCFileSystem(
        url='https://github.com/remla24-team12/model-training.git',
        rev=artifact['rev'],
        config=config
    )

    fs.get_file(artifact['path'], os.path.join("src","model",os.path.basename(artifact['path'])))

def load_secrets(filename='./src/secrets.json'):
    with open(filename, 'r') as file:
        secrets = json.load(file)
    return secrets


if __name__ == "__main__":
    fetch_model()

    app.run(host="0.0.0.0", port=5000, debug=True)
