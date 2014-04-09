import urllib
from bs4 import BeautifulSoup
import urlparse
import mechanize
import re
import sys
from pymongo import MongoClient

def scrapper(start_page, stop_page):
    # Set up mongoDB
    client = MongoClient()
    client = MongoClient('localhost', 27017) 
    db = client.forresterDB
    reports = db.reports

    url_base = 'http://www.forrester.com'
    url_page = 'http://www.forrester.com/search?labelText=&sort=3&range=504005&N=10001&page='   #page number will be appended

    br = mechanize.Browser()

    # Loop through the given page range and open up the URLs
    for current_page in range(start_page, stop_page+1):
        current_url = url_page + str(current_page)
        links = grab_links(br.open(current_url))    # Get links to reports in a list

        # Loop through reports and insert info into the DB
        for item in links:
            link = url_base + item
            print link
            info = grab_info(br.open(link))
            print info
            reports.insert(info)
    
def grab_links(html):
    links = []
    soup = BeautifulSoup(html, 'html5lib')
    for div in soup.find_all('div', class_ = 'num_result_content_anonymous'):
        links.append(div.find('a').get('href'))
    return links

def grab_info(html):
    info = {}
    soup = BeautifulSoup(html, 'html5lib')
    try:
        price = soup.find('span', class_ = 'anonUserBlock').find('span').get_text()
        info['price'] = ''.join(filter(lambda x: x.isdigit(), price))
    except:
        info['price'] = None

    info['authors'] = []
    for a in soup.find('h3', class_ = 'author-name').find_all('a'):
        info['authors'].append(a.get_text())
    return info

def main(argv):
    scrapper(int(argv[0]), int(argv[1]))

if __name__ == '__main__':
   main(sys.argv[1:])
