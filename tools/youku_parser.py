from bs4 import BeautifulSoup
from soupselect import select
import urllib2
import logging
import lxml
import re


def parse_url(url):
    logging.info(url)
    result = urllib2.urlopen(url)
    content = result.read()
    soup = BeautifulSoup(content, "lxml")
    elements = soup.find_all("ul", "v")
    ret = []
    for element in elements:
        ret.append(parse_item(element))
    return ret

def parse_item(video_item):
    ret = {}
    link_element = video_item.find("li", "v_link").find("a")
    ret["video_url"] = link_element["href"]
    ret["title"] = link_element["title"]
    thumb_element = video_item.find("li", "v_thumb").find("img")
    ret["cover_img"] = thumb_element["src"]
    ret["source"] = 'youku'
    ret["external_id"] = parse_youku_id(ret["video_url"])
    return ret
    

ID_REG = re.compile(r"http://v.youku.com/v_show/id_([^\.]+).html")
def parse_youku_id(url):
    match = ID_REG.match(url)
    if match:
        return match.group(1)

    

'''
result = urllib2.urlopen("http://www.youku.com/v_showlist/t2c86g0d3.html")
content = result.read()

soup = BeautifulSoup(content, "lxml")
elements = soup.find_all("ul", "v")
for element in elements:
    print(element)

'''

if __name__ == "__main__":
    elements = parse_url(None)
    for element in elements:
        parse_item(element)
