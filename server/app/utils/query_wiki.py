import wikipediaapi


class WikiSearcher(object):

    def __init__(self) -> None:
        self.wiki = wikipediaapi.Wikipedia('zh')

    def search(self, query):
        page = self.wiki.page(query)
        if page.exists():
            return page
        else:
            return None