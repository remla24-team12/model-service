from flask import Flask, request
from flasgger import Swagger
from lib_ml.preprocessing import process_data

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/', methods=['POST'])
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
              type: string
              example: Safe
    """
    data = request.get_json()
    
    msg = data.get('msg', 'No message received')
    return {"result": msg + " " + process_data("testing the library")}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
