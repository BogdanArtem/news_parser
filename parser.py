from urllib.parse import urljoin
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import os

def open_link(path):
    """Open the link and return the bs object for that link or None"""
    try:
        print(f"Trying to open {path}....")
        html = urlopen(path)
        bs = BeautifulSoup(html.read(), "html.parser")
    except HTTPError as e:
        print(e)
    except URLError:
        print("The server could not be found")
    else:
        print(f"{path} is opened!")
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
    external_links = set()
    internal_links = set()
    articles = set()

    re_external = re.compile('^(http|https)')
    re_internal = re.compile('^(https^|http^|#^|\/).*')
    re_articles = re.compile('^\/a\/.*')

    def find_all_links(base_page):
        global seen
        global external_links
        global internal_links
        global articles

        page = open_link(base_page)
        seen.add(base_page)
        links = get_links(page)

        external_links = (external_links | set(filter(re_external.match, links)))
        internal_links = (internal_links | set(filter(re_internal.match, links)))
        articles = (articles | set(filter(re_articles.match, links)))

        if internal_links - seen == set():
            print("Reached the base case, returning...")
        else:
            for link in internal_links:
                full_path = urljoin(base_page, link)
                if full_path not in seen:
                    find_all_links(full_path)


    find_all_links("https://www.radiosvoboda.org")
    print(articles)
