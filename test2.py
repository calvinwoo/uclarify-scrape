import numpy as np
from statsmodels.formula.api import ols
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn import linear_model
from sklearn.feature_extraction import FeatureHasher
from flask import request

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
    revenue_total = 0
    revenue_real_total = 0

    heading = 'Date,Price,AuthorScore,'
    for elem in range(1,17):
        heading+= 'Role'+str(elem)+','
    heading += 'Predicted Revenue,Actual Revenue'
    print heading

    for elem in range(0, len(predicted_revenue)):
        sample = x_test[elem]
        row = ''

        for var in sample:
            row += str(var)+','
        row += str(predicted_revenue[elem]) + ',' + str(revenues_test[elem])
        print row
        
        total += predicted_revenue[elem] - revenues_test[elem]
        revenue_total += predicted_revenue[elem]
        revenue_real_total += revenues_test[elem]

    num_samples = float(len(predicted_revenue))
    revenue_mean = float(revenue_total)/num_samples
    revenue_real_mean = float(revenue_real_total)/num_samples
    mean = float(total)/num_samples

    std_dev_sum = 0
    for elem in range(0, len(predicted_revenue)):
        difference = predicted_revenue[elem] - revenues_test[elem]
        std_dev_sum += pow(difference - mean, 2)

    variance = float(std_dev_sum)/float(len(predicted_revenue))
    print 'Std Dev:' + str(pow(variance,0.5))
    print 'Difference Mean:' + str(mean)
    print 'Predicted Mean:' + str(revenue_mean)
    print 'Actual Mean:' + str(revenue_real_mean)

def compute_revenue():
    print(request.data)
    authorscore = float(request.data['averageScore'])
    price = float(request.data['price'])
    days = int(request.data['days'])*86400
    role = ROLES_DICT[request.data['role']]
    
    reports = get_reports()
    x_test, x_train = get_x_data()
    revenues = reports['revenue'][0:test_data_length].tolist()

    model = RandomForestRegressor(n_estimators=100)
    model.fit(x_train, revenues)

    sample = [get_sample(days, price, authorscore, role, 16)]
    predicted_revenue = model.predict(sample)
    predicted_revenue = predicted_revenue.tolist()
    return predicted_revenue
    #revenues_test = reports['revenue'][test_data_length:test_data_length*2].tolist()


def get_sample(date, price, authorscore, role, num_roles):
    sample = [date, price, authorscore]
    for _ in range(0, role):
        sample.append(0)
    sample.append(1)
    for _ in range(role+1, num_roles):
        sample.append(0)
    return sample

compute_example_revenue()