### Load Model
import pickle

Model_file = 'Model_C=1.0.bin'
with open("Model_C=1.0.bin", 'rb') as file_in:
    encoded,scaler,model = pickle.load(file_in)

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional

from pydantic import BaseModel

app = FastAPI()

class Customer(BaseModel):
    Gender: str
    Own_car: str
    Own_property: str
    Income_type: str
    Education_level: str
    Marital_status: str
    Way_of_living: str
    Occupation: str
    Employment_status: str
    Nbchildren: int
    Total_income_per_year: float
    Workphone: int
    Phone: int
    Email: int
    Nbfamily_member: Optional[float]
    no_loan: int
    Total_months_credit_registered: int
    Delinquent_accounts: int
    Ordinary_accounts: int
    overall_pastdue: int
    paid_pastdue_diff: int
    Age: int
    Experience: Optional[float]
    Total_income_lifetime_employed: Optional[float]
    Working_year_proportion: Optional[float]

@app.post("/predict")
async def predict(request : Customer):
    test = request.dict()
    # prediction = predict_single_test(test)
    test_encoded = encoded.transform(test)
    test_scaler = scaler.transform(test_encoded)
    y_pred = model.predict_proba(test_scaler)[0,1]

    result = {'risk_proba' : float(y_pred),
        'risk_raito_30' : bool(y_pred >= 0.3)}
    json_compatible_data = jsonable_encoder(result)
    return JSONResponse(json_compatible_data)



# @app.route('/predict', methods =['POST'])
# def predict():
#     test = request.get_json()
#     # prediction = predict_single_test(test)
#     test_encoded = encoded.transform(test)
#     result = test_encoded
#     test_scaler = scaler.transform(test_encoded)
#     y_pred = model.predict_proba(test_scaler)[0,1]
#     risk = y_pred >= 0.3

#     result = {'risk_proba' : y_pred,
#         'risk' :  bool(risk)}
#     return jsonify(result)

# if __name__ == "__main__":
    # app.run(debug = True, host = '0.0.0.0', port  = 9696)