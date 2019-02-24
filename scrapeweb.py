# Using Beautiful Soup library to web scrape sciencedaily.com
from bs4 import BeautifulSoup

# Certification required for Http request
import certifi
import urllib3


http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())


# Takes in the article url and returns only the text within that article
def get_article_text(article_url):
    # Parsing url to HTML tags
    url = article_url
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, features="html.parser")
    final_text = ""

    title = soup.find('h1', {'id': 'headline'}).text
    # There is a '$$$' after the title to help separate it from the rest of the article
    final_text = final_text + title + "$$$"
    # Takes all the <p> tags in the <div> tagged block with id= 'text'
    div = soup.find('div', {'id': 'text'})  # attrs={'id': 'story_text'}
    final_text = final_text + soup.find('p', {'id': 'first'}).text + '%%%'
    for p in div.findAll('p'):
        # '%%%' after each line of text to help with summarizing article
        final_text = final_text + p.text + '%%%'
    return final_text

