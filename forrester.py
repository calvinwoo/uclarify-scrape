import urllib
from bs4 import BeautifulSoup
import urlparse
import mechanize
import re
import sys
import time
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
            print ''
            print link
            info = grab_info(br.open(link))
            # print info
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

    top_section = soup.find('div', class_ = 'analyst-contents')
    # Grab authors
    info['authors'] = []
    for a in top_section.find('h3', class_ = 'author-name').find_all('a'):
        author = a.get_text().strip(' ,')
        info['authors'].append(author)

    # Grab title
    title = top_section.find('h3').get_text()
    info['title'] = title

    # Grab role. "FOR APPLICATION DEVELOPMENT & DELIVERY PROFESSIONALS", remove the first and last words
    role_list = top_section.find('h2').get_text().split()
    role_list.pop()
    role_list.pop(0)
    role = ''
    for word in role_list:
        role = role + word + ' '
    role = role.strip()
    info['role'] = role

    # Grab date. Seconds since 'epoch'
    date_string = top_section.find('span', class_ = 'date').get_text().replace(',', '')    # April 25 2014
    date_string = ' '.join(date_string.split())
    report_date = time.mktime(time.strptime(date_string, '%B %d %Y'))
    todays_date = time.time()
    date = todays_date - report_date
    info['date'] = date

    # Grab price
    try:
        price = soup.find('span', class_ = 'anonUserBlock').find('span').get_text()
        price = ''.join(filter(lambda x: x.isdigit(), price))
    except:
        price = None
    info['price'] = price
    
    # Grab downloads
    info['downloads'] = []
    li = soup.find('ul', class_='resultlist_download').find('li').get_text()
    if 'downloads' in li:
        downloads = li.replace('downloads', '').strip()
    else:
        downloads = '0'
    info['downloads'] = downloads

    # Calculate revenue
    if price is None:
        revenue = None
    else:
        revenue = float(price) * float(downloads)
    info['revenue'] = revenue

    # Grab description
    description = soup.find('div', class_='component_abstract_content').get_text()
    info['description'] = description

    return info

def main(argv):
    scrapper(int(argv[0]), int(argv[1]))

if __name__ == '__main__':
   main(sys.argv[1:])
