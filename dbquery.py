from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.forresterDB
reports = db.reports

roles = {
    'Analyst Relations': [],
    'Application Development & Delivery': [],
    'Business Process': [],
    'CIO': [],
    'Consumer Product Strategy': [],
    'Content & Collaboration': [],
    'CMO': [],
    'Customer Experience': [],
    'Customer Insights': [],
    'eBusiness & Channel Strategy': [],
    'Enterprise Architecture': [],
    'Infrastructure & Operations': [],
    'Marketing Leadership': [],
    'Sales Enablement': [],
    'Security & Risk': [],
    'Sourcing & Vendor Management': []
}

for report in reports.find():
    role = report['role']
    if role is not None:
        revenue = report['revenue']
        if revenue is not None:
            roles[role].append(report['revenue'])

averages = {}
for role, revenues in roles.items():
    count = len(revenues)
    total = 0.0
    for revenue in revenues:
        total = total + revenue
    average = total / count
    averages[role] = average
print averages

f = open('role revenue.csv', 'w')
f.write('role,average'+'\n')
for role, average in averages.items():
    f.write(role+','+str(average)+'\n')
f.close()
