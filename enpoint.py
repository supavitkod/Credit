### Load Model
import pickle

Model_file = 'Model_C=1.0.bin'
with open("Model_C=1.0.bin", 'rb') as file_in:
    encoded,scaler,final_model = pickle.load(file_in)

from flask import Flask
from flask import request
from flask import jsonify


app = Flask('analysis') 

@app.route('/predict', methods =['POST'])
def predict():
    test = request.get_json()
    # prediction = predict_single_test(test)
    test_encoded = encoded.transform(test)
    result = test_encoded
    test_scaler = scaler.transform(test_encoded)
    y_pred = final_model.predict_proba(test_scaler)[0,1]
    risk = y_pred >= 0.3

    result = {'risk_proba' : y_pred,
        'risk' :  bool(risk)}
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0', port  = 9696)