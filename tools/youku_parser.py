from bs4 import BeautifulSoup
from soupselect import select
import urllib2
import logging
import lxml


def parse_url(url):
    result = urllib2.urlopen("http://www.youku.com/v_showlist/t2c86g0d3.html")
    content = result.read()
    logging.info(content)
    soup = BeautifulSoup(content, "lxml")
    elements = soup.find_all("ul", "v")
    return elements 

'''
result = urllib2.urlopen("http://www.youku.com/v_showlist/t2c86g0d3.html")
content = result.read()

soup = BeautifulSoup(content, "lxml")
elements = soup.find_all("ul", "v")
for element in elements:
    print(element)

'''
