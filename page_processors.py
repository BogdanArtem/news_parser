from bs4 import BeautifulSoup


class PageProcesssor:
    def __init__(self, re_target=None):
        self.re_target = re_target

    def parce(self, bs, link):
        pass

    def save(self, texts, header, file_name):
        with open(file_name, "w") as f:
            for paragraph in texts:
                f.write(paragraph.text)
                f.write("\n")
                print(f"File {file_name} is saved")


class SvobodaProcessor(PageProcesssor):
    def parce(self, bs, link):
        """Preprocessor for radiosvoboda.org. Save text of the article in the cuttent dirrectory"""
        try:
            header = bs.find('h1', {'class':'title pg-title'})
            texts = bs.find(id='article-content').find_all('p')
            file_name = header.text.strip('\n') + ".txt"
        except AttributeError:
                print("Looks like article doesn't have header of text")


class EspressoProcessor(PageProcesssor):
    def parce(self):
        pass
