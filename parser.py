from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import re
import os
from datetime import date
from page_processors import SvobodaProcessor

# TODO: Create a separate module for seen and unseen links
class Crawler:
    """Recurcievly open all internal links on a website and call PageProcessor on them"""
    def __init__(self, re_int=None, re_ext=None):
        self.re_int = re.compile('^(https^|http^|#^|\/).*') if re_int is None else re_int
        self.re_ext = re.compile('^(http|https)') if re_ext is None else re_ext


    def crawl(self, main_adress, page_processor=None):
        """Open all links inside the website and do some processing on them"""
        main = self.open_link(main_adress)
        links = self.get_links(main)
        internal_links, external_links = self.parse_links(links, self.re_int, self.re_ext, main_adress)

        # Create a new directory to gather data
        self.initialize_dir()

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
                    page = self.open_link(link)

                    #do some processing on the page
                    if page_processor:
                        page_processor(page, link)

                    seen.add(link)
                    to_check.remove(link)
                    links = self.get_links(page)
                    to_check = (to_check | (self.parse_links(links, self.re_int, self.re_ext, main_adress)[0] - seen))


    def open_link(self, path):
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


    def get_links(self, bs):
        """Accepts Beautifulsoup object, returns set of links"""
        if bs is not None:
            links = set()
            for link in bs.find_all('a'):
                if 'href' in link.attrs:
                    links.add(link['href'])
            return set(links)
        else:
            print("Can't find links for None")
            return set()

    def parse_links(self, links, re_internal, re_external, base_link):
        external_links = set(filter(re_external.match, links))
        internal_links = set(filter(re_internal.match, links))
        full_internal_links = set([urljoin(base_link, x) for x in internal_links])
        return full_internal_links, external_links


    def initialize_dir(self):
        """Create new directory with current date as name and make it a workdir"""
        folder_name = date.today().__str__()
        if not os.path.exists(os.path.join(os.getcwd(), folder_name)):
            os.mkdir(folder_name)
            os.chdir(folder_name)


if __name__ == '__main__':
    crawler = Crawler()
    crawler.crawl("https://www.radiosvoboda.org")


