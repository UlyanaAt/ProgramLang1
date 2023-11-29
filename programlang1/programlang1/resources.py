import requests
from bs4 import BeautifulSoup


class Resources:

    def __init__(self):
        self.data: list = []

    def get_articles(self, resource: int) -> list:
        if resource == 1:
            html = requests.get('https://www.nbcnews.com/us-news').text
            result = self.nbcnews(html=html)
            return result
        if resource == 2:
            html = requests.get('https://www.washingtonpost.com/politics/').text
            result = self.washingtonpost(html=html)
            return result
        if resource == 3:
            html = requests.get('https://www.cbsnews.com/us/').text
            result = self.cbsnews(html=html)
            return result

    def nbcnews(self, html: str) -> list:
        soup = BeautifulSoup(html, "html.parser")

        articles: list | None = None

        moreNews = soup.find('div', class_='styles_itemsContainer__saJYW')
        news = moreNews.find_all('wide-tease-item__wrapper df flex-column flex-row-m flex-nowrap-m')
        
        for new in soup.find(id="news-feed-container").find_all('article'):
            header = new.find('h3', class_='gc__title').find('span').text.replace('\xad', '')

            if header not in self.data:
                self.data.append(header)

                article = {
                    'header': header,
                    'annotation': new.find('div', class_='gc__excerpt').find('p').text.replace('\xad', ''),
                    'date': new.find('div', class_='gc__date__date').find('span').text.replace('Published On ', '')
                }

                if articles is None:
                    articles = [article]
                else:
                    articles.append(article)

            return articles

    def washingtonpost(self, html: str) -> list:
        soup = BeautifulSoup(html, "html.parser")

        main = soup.find('div', class_='colMain')
        dates = main.find_all('h4', class_='redHead')

        articles: list | None = None
        for index, block in enumerate(
                main.find_all(
                    'ul',
                    class_='leads',
                )
        ):
            for new in block.find_all('li'):
                header: str = new.find('h3', class_='smallCaps').find('a').text.replace('\xa0', ' ')

                if header not in self.data:
                    self.data.append(header)

                    article = {
                        'header': header,
                        'annotation': new.find('p').text.replace('\xa0', ' ').replace(' czytaj więcej', ''),
                        'date': dates[index].text.replace('\xa0', ' ')
                    }

                    if articles is None:
                        articles = [article]
                    else:
                        articles.append(article)
        return articles

    def cbsnews(self, html: str) -> list:
        soup = BeautifulSoup(html, "html.parser")

        articles: list | None = None
        for new in soup.findAll('div', class_='list_info'):
            header: str = new.find('a', class_='new_title_ms').text

            if header not in self.data:
                self.data.append(header)

                other: list[str] = new.find(
                    'div',
                    class_='source_time',
                ).text.split('|')

                article = {
                    'header': header,
                    'annotation': new.find('p').text,
                    'author': other[0].replace('By ', ''),
                    'date': other[1].split(' ')[2]
                }

                if articles is None:
                    articles = [article]
                else:
                    articles.append(article)
            return articles
