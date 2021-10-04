import string
import time

import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

baseurl = "https://www.indifferentlanguages.com"
urls= []
parser = 'html.parser'
resp = requests.get(baseurl)
http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
encoding = html_encoding or http_encoding
soup = BeautifulSoup(resp.content, parser, from_encoding=encoding)

for link in soup.find_all('a', class_="letter"):
    urls.append(baseurl + link['href'])

# allurls = []
allurls = set()
for item in urls:
    reqs = requests.get(item)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    for link in soup.find_all('a'):
        extension = link.get('href')
        if "dictionary" in extension:
            # allurls.append(baseurl + extension)
            allurls.add(baseurl + extension)
            print(baseurl + extension)
        
# print(allurls)