from flask import Flask
from flask import render_template, json
import os
import numpy as np
from statsmodels.formula.api import ols
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn import linear_model
from sklearn.feature_extraction import FeatureHasher
from flask import request
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

app = Flask(__name__)
app.debug = True
@app.route('/')
def hello_world():
    return render_template('analysis.html')

@app.route('/authorscore')
def authorscore():
	f = open(os.path.join(BASE_DIR, "authorandscore.json"), "r")
	data = f.read()
	f.close()
	#data = json.load(json_data)
	return data


test_data_length = 1000
ROLES_DICT = {'CMO': 3, 'Infrastructure & Operations': 9, 'Application Development & Delivery': 4, 'Sales Enablement': 11, 'CIO': 2, 'Marketing Leadership': 5, 'Content & Collaboration': 15, 'Enterprise Architecture': 1, 'Security & Risk': 6, 'Business Process': 14, 'eBusiness & Channel Strategy': 0, 'Analyst Relations': 12, 'Consumer Product Strategy': 13, 'Sourcing & Vendor Management': 8, 'Customer Insights': 7, 'Customer Experience': 10}


def get_reports():
    reports = pd.read_csv('reportswithscore.csv', 
                          sep=',', 
                          names=['title', 'role', 'date', 'authors', 'authorscore', 'price', 'downloads', 'revenue'], 
                          skiprows=1)

    reports = reports.dropna()
    return reports

def get_x_data():
    reports = get_reports()
    #print(reports)
    #reports3 = reports[pd.notnull(reports['price'])]

    raw_roles = reports['role']
    dates = reports['date'].tolist()
    prices = reports['price'].tolist()
    authorscores = reports['authorscore'].tolist()

    roles = []
    #role_dict = {}
    counter = 0
    for role in raw_roles:
        #if role in role_dict:
        #    role_num = role_dict[role]
        #    roles.append(role_num)
        #else:
        #    role_dict[role] = counter
        #    roles.append(counter)
        #    counter += 1
        roles.append(ROLES_DICT[role])

    #print role_dict
    #num_roles = len(role_dict)
    num_roles = 16

    x_train = []
    for elem in range(0, test_data_length):
        sample = get_sample(dates[elem], prices[elem], authorscores[elem], roles[elem], num_roles)
        x_train.append(sample)

    x_test = []
    for elem in range(test_data_length, test_data_length*2):
        sample = get_sample(dates[elem], prices[elem], authorscores[elem], roles[elem], num_roles)
        x_test.append(sample)

    return [x_test, x_train]
    

def compute_example_revenue():
    reports = get_reports()
    x_test, x_train = get_x_data()
    revenues = reports['revenue'][0:test_data_length].tolist()

    model = RandomForestRegressor(n_estimators=100)
    model.fit(x_train, revenues)

    predicted_revenue = model.predict(x_test)
    predicted_revenue = predicted_revenue.tolist()
    revenues_test = reports['revenue'][test_data_length:test_data_length*2].tolist()

    diff_list = []
    total = 0

    for elem in range(0, len(predicted_revenue)):
        print 'predicted_revenue:' + str(predicted_revenue[elem]) + ' Real:' + str(revenues_test[elem])
        total += predicted_revenue[elem] - revenues_test[elem]
    mean = float(total)/float(len(predicted_revenue))

    std_dev_sum = 0
    for elem in range(0, len(predicted_revenue)):
        difference = predicted_revenue[elem] - revenues_test[elem]
        std_dev_sum += pow(difference - mean, 2)

    variance = float(std_dev_sum)/float(len(predicted_revenue))
    print(pow(variance,0.5))

@app.route('/get_money')
def compute_revenue():
    print(request.args)
    print('------------------------------')
    authorscore = float(request.args['averageScore'])
    price = float(request.args['price'])
    days = int(request.args['days'])*86400
    role = ROLES_DICT[request.args['role']]
    
    reports = get_reports()
    x_test, x_train = get_x_data()
    revenues = reports['revenue'][0:test_data_length].tolist()

    model = RandomForestRegressor(n_estimators=100)
    model.fit(x_train, revenues)

    sample = [get_sample(days, price, authorscore, role, 16)]
    predicted_revenue = model.predict(sample)
    predicted_revenue = predicted_revenue.tolist()
    print(predicted_revenue[0])
    print('------------------------------')
    return str(predicted_revenue[0])
    #revenues_test = reports['revenue'][test_data_length:test_data_length*2].tolist()


def get_sample(date, price, authorscore, role, num_roles):
    sample = [date, price, authorscore]
    for _ in range(0, role):
        sample.append(0)
    sample.append(1)
    for _ in range(role+1, num_roles):
        sample.append(0)
    return sample


if __name__ == '__main__':
    app.run()