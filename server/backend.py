from flask import Flask, jsonify, request
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

# Provides data through this URL (API endpoint)
@app.route('/api/data', methods=['GET'])
def get_data():
    # Get page and size from query parameters, with default values //paging technique taught in os hehe
    page = int(request.args.get('page', 1))  # Default to page 1
    size = int(request.args.get('size', 100))  # Default page size is 100

    # Read specific chunks of the dataset
    skip_rows = (page - 1) * size
    try:
        chunk = pd.read_csv(DATA_FILE, skiprows=range(1, skip_rows + 1), nrows=size, header=0)
        data = chunk.to_dict(orient="records")
        return jsonify({"page": page, "size": size, "data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
