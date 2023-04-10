#### CRISP-DM FRAMEWORK End to End
### Credit card approval prediction data from Kaggle
## 1.Business understanding
Credit score cards are a common tool used by financial institutions to assess the creditworthiness of credit card applicants.

![Alt text](Image/dataset-cover.jpg)

# Objective:
The main objective of using credit score cards is to predict the probability of future defaults and credit card borrowings by the applicant, allowing the bank to make informed lending decisions. As the bank will benefit in term of :
Improved Risk Management: By accurately assessing the risk associated with lending to a particular customer, the bank can minimize its potential losses.
Better Lending Decisions: With a better understanding of a customer's credit history and financial situation, the bank can make more informed lending decisions and minimize the risk of loan default.
Increased Profitability: By lending to customers with a good credit history, the bank can increase its profitability by charging higher interest rates and fees.
Improved Customer Relationships: By offering tailored loan products and services based on a customer's credit history, the bank can improve customer satisfaction and strengthen customer relationships.


Determining a customer's creditworgithiness is a crucial aspect of risk management for banks. By using credit score cards, banks can make informed lending decisions that are in their best interests and the best interests of their customers. This leads to improved risk management, better lending decisions, increased profitability, and improved customer relationships.

## 2. Data Understanding

# Data collection
The dataset utilized for this project was obtained from Kaggle, an online community of data scientists and machine learning enthusiasts. The dataset contains two distinct tables, each of which includes a total of 21 different columns. In depth, there're 13 categorical variables, 6 continous variables , and 2 ID variables.

The first table pertains to demographic data and encompasses a range of variables, such as age, gender, marital status, and other relevant information regarding the customers.

The second table relates to credit status data, which entails information about the customers' credit history, including the number of months elapsed since their last payment and whether or not they have paid off their debts. This information allows for the creation of a time frame during which the customer either failed to pay their loan on time or successfully paid off their debt.

In summary, the dataset utilized in this project contains two distinct tables with multiple columns that provide crucial demographic and credit status information about the customers. Such information is essential in the evaluation of the risk associated with lending to individuals and plays a crucial role in decision-making processes for financial institutions.

# Data Exploration

Based on the available data, it appears that the majority of users are considered to be "risky," with 99% of users falling into this category. Furthermore, 69% of users are single individuals. The most frequently reported total income is 135,000 dollars, and all users have provided a mobile phone number. However, only 10% of users have provided an email address.

It is interesting to note that the highest average income is reported by users with 19 children in their family, and there is a positive correlation between income and the number of family children. Additionally, the most common age among users is 40 years old.

The majority of users (66%) are female, with male users recording the highest reported income at $217,869. 40% of users own a car, and 65% of users own a property. Half of the users are employed, with commercial associates having the highest average income.

67% of users have a secondary level of education, while higher education is associated with the maximum income. 70% of users are married, with single or unmarried individuals having a higher reported income. Finally, 89% of users have a house, and 99% of users have been deemed too risky to qualify for a credit card.

In addition, it can be observed that the majority of customers tend to pay off their loans within a relatively short period, ranging from 1 to 29 days. Furthermore, a significant percentage of customers do not borrow loans at all.

It is also noteworthy that a high percentage of customers pay off their loans entirely, indicating a responsible approach to borrowing and repayment. However, the data also suggests that there are some customers who are late in paying off their loans.




## 3.Data preparation

# Cleaning Data
The given Datasets from Kaggle that I've worked on it's come in a pretty good term as the data only have missing values as there's none duplicate values.In this particular scenario, it has been identified that only one feature, namely the occupation feature, has missing values.

The presence of missing values in a dataset can be attributed to various factors, such as data entry errors, data corruption, or incomplete data collection. The most common approaches to handling missing values are imputation and deletion. Imputation involves filling in the missing values with an estimated value, whereas deletion involves removing the entire record that contains the missing value.

In this case, the chosen approach to handle the missing values is imputation. Specifically, the missing values in the occupation feature will be replaced with the value 'other.' This approach is reasonable since it allows us to retain the information contained in the other features of the record while acknowledging the absence of information for the occupation feature.

# Outliers
During the exploratory data analysis, it was observed that some of the numerical features had outliers. Outliers are extreme values that are significantly different from other values in the dataset. These outliers can have a considerable impact on the model's performance and may need to be addressed.

To address the outliers, the percentile method was used to trim the data for some features such as Nbchildren and total_income_per_year. The percentile method involves setting a threshold at the maximum and minimum values of a feature, and any value that exceeds this threshold is considered an outlier and removed from the dataset. This method was chosen as it removes insignificant outliers that do not provide valuable information to the model.

However, the feature DAYS_EMPLOYED also had extreme outliers. It was decided not to remove these outliers as they represent individuals who did not get employed. This factor could be useful in the feature engineering process, where the outliers will be used to create a new feature or modify an existing one.

# Feature Engineering
After the process of the exploratory data anlysis, as the data is limited and in order to improve the effiency when runing the model, I've applied the process of feature engineering. 
## 4.Model Selection


## 5.Deployment
# Save and load Model by using pickle
When working with machine learning models, it is important to save them so that they can be used later for making predictions or for further analysis. One common way to do this is by using the pickle module in Python. picklcan serialize Python objects, which means that I can convert them into a format that can be saved to disk and loaded back into memory later.
In my case, I have a Xgbmodel  along with some other objects that are needed to make predictions with the model. Specifically, I have a scaler object, a dictvectorizer object, and an XGBoost model. The scaler and dictvectorizer are used to preprocess input data before it is fed into the model, and the XGBoost model is the actual machine learning model that makes the predictions.
To save these objects, I use pickle.dump() to write them to a binary file on disk. This file can then be loaded back into memory later using pickle.load(). Thus, When I load the objects back into memory, I can use them to make predictions on new input data without having to retrain the model.

# Flask
Flask is a micro web framework written in Python that allows you to easily create web applications and RESTful web services. It is lightweight and flexible, making it a popular choice for building small to medium-sized web applications.
With Flask, I can define routes for different HTTP methods such as GET, POST, PUT, and DELETE. I can define templates for rendering HTML pages, handle form submissions, and interact with databases.
To get started with Flask, I install it using pip, the Python package manager. Once installed, I create a new Flask application by defining a Python script with the necessary routes and functions.
```python
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
    y_pred = model.predict_proba(test_scaler)[0,1]
    risk = y_pred >= 0.3

    result = {'risk_proba' : y_pred,
        'risk' :  bool(risk)}
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0', port  = 9696)
```

This code creates a Flask web service that responds to requests on the '/predict URL path with the results of our model. When run directly, the application runs in debug mode on port 9696 of the local machine, and is accessible to other devices on the network via the IP address '0.0.0.0'.





# How to run web server
# Local
pipenv shell
uvicorn enpoint-fast:app --host 0.0.0.0 --port 9696 --reload

```bash
docker build -t predict_fast .
```

```bash
docker run -it -p 9696:9696 --rm predict_fast
```

docker run -it -p 9696:9696 --rm predict_fast 



conda deactivate, conda activate
# cloud







