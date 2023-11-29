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
        news = moreNews.find_all('div', class_='wide-tease-item__wrapper df flex-column flex-row-m flex-nowrap-m')
        
        for new in news:
            header = new.find('h2', class_='wide-tease-item__headline').text 
            
            if header not in self.data:
                self.data.append(header)

                article = {
                    'header': header,
                    'annotation': new.find('div', class_='wide-tease-item__description').text,
                    'date': new.find('div', class_='wide-tease-item__timestamp dib db-m ml3 ml0-m').text
                }
                
                if articles is None:
                    articles = [article]
                else:
                    articles.append(article)

        return articles

    def washingtonpost(self, html: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        
        articles: list | None = None
        
        main = soup.find('article', class_='b-l br-l mb-xxl-ns mt-xxs mt-md-l pr-lg-l col-8-lg mr-lg-l')
        news = main.find_all(attrs={"data-feature-id": True})
        
        for new in news:
            header = new.find('h3').text 
            
            if header not in self.data:
                self.data.append(header)

                article = {
                    'header': header,
                    'annotation': new.find('p', class_='pt-xs pb-xs font-size-blurb lh-fronts-tiny font-light gray-dark dn db-ns').text,
                    'author': new.find('a', class_='wpds-c-knSWeD wpds-c-knSWeD-iRfhkg-as-a').text,
                    'date': new.find('span', class_='wpds-c-iKQyrV font-xxxs font-light font--meta-text lh-sm gray-dark dot-xxs-gray-dark').text
                }
                
                if articles is None:
                    articles = [article]
                else:
                    articles.append(article)

        return articles

    def cbsnews(self, html: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        
        articles: list | None = None
        
        main = soup.find('section', class_='component list-river list list-river--with-hero list-river--with-load-more --has-view-more component--topic- component--view-list-river-with-hero-with-load-more --item-count-15')
        news = main.find_all('a', class_='item__anchor')
        
        for new in news:
            header = new.find('div', class_='item__title-wrapper').find('h4', class_='item__hed').text.replace('\n                    ', '')
            
            if header not in self.data:
                self.data.append(header)

                article = {
                    'header': header,
                    'annotation': new.find('p', class_='item__dek').text.replace('\n        ', ""),
                    'date': new.find('li', class_='item__date').text
                }
                
                if articles is None:
                    articles = [article]
                else:
                    articles.append(article)

        return articles