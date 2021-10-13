from bs4 import BeautifulSoup
import requests
import string
import time
import itertools 
import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import json


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
            
        
# print(allurls)
finale = set()
for item in allurls:
    reqs = requests.get(item)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    for link in soup.find_all('a'):
        extension = link.get('href')
        if "word" in extension:
            # allurls.append(baseurl + extension)
            finale.add(baseurl + extension)

def get_woord(item):
    splitted_word = item.split("/")[-1]
    return splitted_word


def get_category(item):
    request = requests.get(item)
    html_soup = BeautifulSoup(request.text, "html.parser")
    categories = html_soup.find_all('div', class_="word-categories")
    categories = str(categories).split("href")
    category_list = [item.split("/")[2].split('"')[0] for item in categories if "category" in item]
    return category_list

def get_translation(item):
    reqs = requests.get(item)
    html_soup = BeautifulSoup(reqs.text, "html.parser")
    languages = html_soup.find_all('td', class_='language-name')
    translation_dict = {}
    for language in languages:
        try:
            language = str(language)
            country = language.split("lang")[1].split(">")[2].split('<')[0]
            translation = language.split("lang=")[1].split(">")[1].split("<")[0]
            translation_dict[country] = translation
            time.sleep(0.1)
        except:
            continue
    return translation_dict

for item in finale:
    get_woord(item)
    fun = get_woord(item)
    get_category(item)
    lolz = get_category(item)
    get_translation(item)
    omg = get_translation(item)
    data[fun] = {"categories": (lolz) , "translations": (omg)}

with open("indifferent_languages.json", "w") as fp:
    json.dump(data, fp)


