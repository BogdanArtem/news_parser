from urllib.parse import urljoin
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import os

def open_link(path):
    """Open the link and return the bs object for that link or None"""
    try:
        html = urlopen(path)
        bs = BeautifulSoup(html.read(), "html.parser")
    except HTTPError as e:
        print(e)
    except URLError:
        print("The server could not be found")
    else:
        print(f"{path} is opened")
        return bs


def save_article(bs):
    """Accepts BS object. Save text of the article in the cuttent dirrectory"""
    try:
        header = bs.find('h1', {'class':'title pg-title'})
        texts = bs.find(id='article-content').find_all('p')
        file_name = header.text.strip('\n') + ".txt"
        with open(file_name, "w") as f:
            for paragraph in texts:
                f.write(paragraph.text)
                f.write("\n")
        print(f"File {file_name} is saved")
    except AttributeError:
            print("Looks like article doesn't have header of text")


def get_links(bs):
    """Accepts Beautifulsoup object, returns set of links"""
    links = set()
    for link in bs.find_all('a'):
        if 'href' in link.attrs:
            links.add(link['href'])
    return set(links)


if __name__ == '__main__':
    # Collect all links
    seen = set()
    base_page = "https://www.radiosvoboda.org"

    page = open_link(base_page)
    links = get_links(page)

    re_external = re.compile('^(http|https)')
    external_links = list(filter(re_external.match, links))

    re_internal = re.compile('^(https^|http^|#^|\/).*')
    internal_links = list(filter(re_internal.match, links))

    print(internal_links)
    # Define links to explore
## Find articles
## Find trash links
## Find liks to explore


# Open defined links

# Check if you have new links

