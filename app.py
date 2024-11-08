import subprocess
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from the backend!"})

def run_electron():
    try:
        subprocess.run(["npm", "start"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error starting Electron:", e)

if __name__ == "__main__":
    electron_process = subprocess.Popen(["npm", "start"], shell=True)

    try:
        app.run(port=5000) 
    finally:
        electron_process.terminate()
