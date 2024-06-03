import subprocess

def pull_from_dvc():
    subprocess.run(['pipenv', 'shell'])
    subprocess.run(['dvc', 'init'])
    result = subprocess.run(['dvc', 'pull', 'data/better_labels.txt'], capture_output=True, text=True)
    return result.stdout

def push_to_dvc():
    subprocess.run(['dvc', 'add', 'data/better_labels.txt'], capture_output=True, text=True)
    result = subprocess.run(['dvc', 'push'], capture_output=True, text=True)
    return result.stdout