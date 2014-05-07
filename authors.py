import csv
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.forresterDB
reports = db.reports

author_revenues = {}
author_average = {}

for report in reports.find():
    authors = report['authors']
    revenue = report['downloads']
    if revenue is None:
        revenue = 0
    else:
        revenue = float(revenue)
    for author in authors:
        if author not in author_revenues:
            author_revenues[author] = [revenue]
        else:
            author_revenues[author].append(revenue)

for author, revenues in author_revenues.items():
    average_revenue = sum(revenues) / float(len(revenues))
    author_average[author] = average_revenue

with open('reportswithscore.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(['title', 'role', 'date', 'authors', 'authorscore', 'price', 'downloads', 'revenue'])
    for report in reports.find():
        if len(report['authors']) is 0:
            average_score = 0
        else:
            score_total = 0
            count = 0
            for author in report['authors']:
                score_total = score_total + author_average[author]
                count = count + 1
            average_score = score_total / count
        writer.writerow([report['title'].encode('ascii', 'ignore'), report['role'], report['date'], report['authors'], average_score, report['price'], report['downloads'], report['revenue']])
