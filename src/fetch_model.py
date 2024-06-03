import os
import json
import dvc.api


def fetch_model():
    """
    Fetch model and tokenizer from dvc registry
    """

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