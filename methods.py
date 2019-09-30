import random
from pyquery import PyQuery as pq


def parse_qa_url(response):
    d = pq(response.text)
    content_list = d('a.question__title-link.question__title-link_list')
    return pq(content_list[random.randrange(1, len(content_list), 1)]).attr('href')

