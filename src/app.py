from flask import Flask, jsonify
from src.predict import score_customer
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/score/<customer_id>')
def get_score(customer_id):
    prob = score_customer(customer_id)
    if prob is None:
        return jsonify({'error':'not found'}),404
    return jsonify({'customer_id':customer_id,'purchase_probability':float(prob)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
