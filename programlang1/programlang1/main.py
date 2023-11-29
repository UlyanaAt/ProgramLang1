from threading import Thread
from queue import Queue
from time import (sleep, time)
from programlang1.resources import Resources


def scraper(number: int, obj: Resources, queue: Queue) -> None:
    articles: list = obj.get_articles(resource=number)
    for article in articles:
        queue.put(article)


def update(queue: Queue, obj: Resources) -> None:
    print('------')
    for number in range(1, 4):
        Thread(target=scraper, args=(number, obj, queue),).start()


if __name__ == '__main__':
    res: Resources = Resources()

    q = Queue()

    start = time()
    update(queue=q, obj=res)

    while True:
        if (time() - start) >= 60:
            start = time()
            update(queue=q, obj=res)
        if not q.empty():
            print(q.get())
            sleep(0.5)
