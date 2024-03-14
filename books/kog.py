import os
import re
import requests
from selectolax.parser import HTMLParser
from utils.upload import *
from utils.rss import RSSFeed


BOOK_LIST = [
    ["高手", "https://www.56kog.com/list/15/15314_24.html", "xhdtsgs.rss"],
    ["人道大圣", "https://www.56kog.com/list/203/203113_5.html", "rdds.rss"]
]


def get_text_selectolax(html):
    tree = HTMLParser(html)

    if tree.body is None:
        return None

    for tag in tree.css('script'):
        tag.decompose()
    for tag in tree.css('style'):
        tag.decompose()

    text = tree.body.text(separator='')
    return text


def parse(history_path='./'):
    for book in BOOK_LIST:
        rss_feed = RSSFeed(book[0], '')
        if os.path.exists(history_path + book[2]):
            rss_feed.load(history_path + book[2])
        try:
            rss_feed = RSSFeed(book[0], '')
            if os.path.exists(history_path + book[2]):
                rss_feed.load(history_path + book[2])
            response = requests.get(book[1], timeout=10)
            response.encoding = "gbk"
            html = response.text
            tree = HTMLParser(html)
            html_list = tree.tags('el-tag')
            html_list.reverse()
            count = 0
            for h in html_list:
                m = re.match(r".*'(.+?)','_self'.+?>(.+?)</el-tag>", h.html)
                if m:
                    name = m[2]
                    count = count + 1
                    if rss_feed.exist(name) is False:

                        link = m[1].encode('utf8').decode('unicode_escape')
                        response = requests.get(f'https://www.56kog.com{link}', timeout=30)
                        response.encoding = "gbk"
                        html_content = response.text
                        rss_feed.add_item(name,
                                          get_text_selectolax(html_content).replace(" ", "").replace("\n\n", "</br>").replace("\n", "</br>"),
                                          f'https://www.56kog.com{link}')
                    if count >= 20:
                        break
            rss_feed.save(history_path + book[2])
            print('Upload to server: {}'.format(book[2]))
            upload_to_server(history_path + book[2])
        except Exception as ex:
            rss_feed.save(history_path + book[2])
            print('Upload to server: {}'.format(book[2]))
            upload_to_server(history_path + book[2])
            raise ex


if __name__ == '__main__':
    parse('../rss/')
