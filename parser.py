from urllib.parse import urljoin, quote
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
    except UnicodeEncodeError:
        print(f"Non unicode path! {path} is skipped ")
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


def parse_links(links, re_internal, re_external, base_link):
    external_links = set(filter(re_external.match, links))
    internal_links = set(filter(re_internal.match, links))
    articles = set(filter(re_articles.match, links))
    full_internal_links = set([urljoin(base_link, x) for x in internal_links])
    return full_internal_links, external_links


if __name__ == '__main__':
    # Set up filters to scan a website
    re_external = re.compile('^(http|https)')
    re_internal = re.compile('^(https^|http^|#^|\/).*')
    re_articles = re.compile('^\/a\/.*')

    # First iteration
    base_link = "https://www.radiosvoboda.org"
    main = open_link(base_link)
    links = get_links(main)
    internal_links, external_links = parse_links(links, re_internal, re_external, base_link)

    seen = set()
    to_check = set(internal_links)
    while to_check != set():
        print("-"*50)
        print(f"Length of seen is {len(seen)}")
        print(f"Length of unseen is {len(to_check)}")
        print("-"*50)
        to_check_copy = to_check.copy()
        for link in to_check_copy:
            if link not in seen:
                page = open_link(link)
                seen.add(link)
                to_check.remove(link)
                links = get_links(page)
                to_check = (to_check | (parse_links(links, re_internal, re_external, base_link)[0] - seen))
