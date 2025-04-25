from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'File Comparison API is running!'

@app.route('/compare-files', methods=['POST'])
def compare_files():
    try:
        file1 = request.files['file1']
        file2 = request.files['file2']
        key1 = request.form.get('key1')
        key2 = request.form.get('key2')

        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)

        merged = df1.merge(df2, left_on=key1, right_on=key2, how='outer', indicator=True)
        merged['Match Status'] = merged['_merge']
        merged.drop(columns=['_merge'], inplace=True)

        return merged.to_json(orient='records')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
