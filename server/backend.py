from flask import Flask, jsonify
import pandas as pd
import os
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)
# Load preprocessed data
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "covid_data_mexico.csv")

try:
    aggregated_data = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    aggregated_data = None
    print(f"Error: Data file not found at {DATA_FILE}")

@app.route('/')
def home(): #base page
    return "Backend is working. Please access /api/data for JSON data."

#provides data through this url (API endpoint)
@app.route('/api/data', methods=['GET'])
def get_data():
    if aggregated_data is not None: #data is not null
        print("Backend works.")
        return jsonify(aggregated_data.to_dict(orient='records'))
    else:
        return jsonify({"error": "Data file not found or could not be loaded."}), 500

if __name__ == '__main__':
    app.run(debug=True)
