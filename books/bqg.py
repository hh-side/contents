import time
from html.parser import HTMLParser
from utils.messages import *
from utils.upload import *
from utils.rss import RSSFeed


BOOK_LIST = [["人道大圣", "https://www.ishuquge.la/txt/12236/index.html", "bqg_rdds.rss"]]


class ChaptersHTMLParser(HTMLParser):
    def error(self, message):
        print(message)
        pass

    def __init__(self):
        HTMLParser.__init__(self)
        self.chapters = []
        self.inRightTags = False
        self.chapterLink = ''

    def handle_starttag(self, tags, attrs):
        if tags == 'div':
            for (name, value) in attrs:
                if name == 'class' and value == 'listmain':
                    self.inRightTags = True
        if self.inRightTags and tags == 'a':
            for (name, value) in attrs:
                if name == 'href':
                    self.chapterLink = value

    def handle_endtag(self, tags):
        if tags == 'div':
            self.inRightTags = False

    def handle_data(self, data):
        if self.chapterLink != '':
            self.chapters.append({
                "name": data,
                "link": self.chapterLink
            })
            self.chapterLink = ''


class ContentHTMLParser(HTMLParser):
    def error(self, message):
        print(message)
        pass

    def __init__(self):
        HTMLParser.__init__(self)
        self.content = ''
        self.currentLink = ''
        self.next = ''
        self.inRightTags = 0
        self.isContent = False

    def handle_starttag(self, tags, attrs):
        if tags == 'div':
            for (name, value) in attrs:
                if name == 'id' and value == 'content':
                    self.inRightTags += 1
                if name == 'id' and value == 'center_tip':
                    self.inRightTags += 1

    def handle_endtag(self, tags):
        if self.inRightTags > 0 and tags == 'div':
            self.inRightTags -= 1

    def handle_data(self, data):
        if self.inRightTags > 0:
            self.content += str(data).strip() + '</br>'


def parse(history_path='./'):
    chapters_parser = ChaptersHTMLParser()
    content_parser = ContentHTMLParser()
    for book in BOOK_LIST:
        try:
            rss_feed = RSSFeed(book[0], '')
            if os.path.exists(history_path + book[2]):
                rss_feed.load(history_path + book[2])
            response = requests.get(book[1], timeout=30)
            response.encoding = 'utf-8'
            html = response.text
            chapters_parser.chapters = []
            chapters_parser.feed(html)
            for chapter in chapters_parser.chapters[-20:]:
                if rss_feed.exist(chapter['name']) is False:
                    print(f'New chapter {chapter["name"]}')
                    try:
                        content_url = book[1].replace('index.html', chapter['link'])
                        content_parser.content = ''
                        response = requests.get(content_url, timeout=30)
                        response.encoding = 'utf-8'
                        html = response.text
                        content_parser.feed(html)
                        if content_parser.content.find('正在手打中') < 0:
                            print(f'New chapter ready!!! {chapter["name"]}')
                            rss_feed.add_item(chapter['name'],
                                              content_parser.content,
                                              chapter['link'])
                            push_wechat_message('{} - {}'.format(book[0], chapter['name']), link=chapter['link'])
                    except Exception as ex:
                        print(ex)
            print(book)
            rss_feed.save(history_path + book[2])
            print('Upload to server: {}'.format(book[2]))
            upload_to_server(history_path + book[2])
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    parse('../rss/')
