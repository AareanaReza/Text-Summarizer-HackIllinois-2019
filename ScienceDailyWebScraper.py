# Using Beautiful Soup library to web scrape sciencedaily.com
from bs4 import BeautifulSoup

# Certification required for Http request
import certifi
import urllib3

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

url = 'https://www.sciencedaily.com/releases/2019/02/190221141511.htm'
response = http.request('GET', url)
soup = BeautifulSoup(response.data, features="html.parser")

div = soup.find('div', {'id': 'text'})  # attrs={'id': 'story_text'}
print(soup.find('p', {'id': 'first'}).text)
for p in div.findAll('p'):
    print(p.text)
