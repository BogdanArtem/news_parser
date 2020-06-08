import os
from datetime import date
from abc import abstractmethod
from bs4 import BeautifulSoup


class PageProcesssor:
    def __init__(self, re_target=None):
        self.re_target = re_target

    @abstractmethod
    def parce(self, bs, link):
        pass

    def save(self, texts, header, file_name):
        """Save header and text as .txt file"""
        with open(file_name, "w") as f:
            for paragraph in texts:
                f.write(paragraph.text)
                f.write("\n")
            print(f"File {file_name} is saved")
            print("-"*50, "\n")

    def is_valid(self, link):
        """Check if link matches to the target regex"""
        if self.re_target.match(link):
            return True
        else:
            return False

    def initialize_dir(self):
        """Create new directory with current date as name and make it a workdir"""
        folder_name = date.today().__str__()

        if folder_name not in os.getcwd():
            if not os.path.exists(os.path.join(os.getcwd(), folder_name)):
                os.mkdir(folder_name)
                os.chdir(folder_name)
            os.chdir(folder_name)

    def process(self, bs, link):
        """Combine all the previous methods to process the page"""
        try:
            self.initialize_dir()
            self.save(*self.parce(bs, link))
        except TypeError:
            print("Skiped this link for saving...")
            print("-"*50, "\n")


class SvobodaProcessor(PageProcesssor):
    def parce(self, bs, link):
        """Preprocessor for radiosvoboda.org. Save text of the article in the cuttent dirrectory"""
        if self.is_valid(link):
            try:
                header = bs.find('h1', {'class':'title pg-title'})
                texts = bs.find(id='article-content').find_all('p')
                file_name = header.text.strip('\n') + ".txt"
                return texts, header, file_name
            except AttributeError:
                print("Looks like article doesn't have header of text")
