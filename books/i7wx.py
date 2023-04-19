from html.parser import HTMLParser
from utils.messages import *
from utils.rss import RSSFeed


BOOK_LIST = [["高手", "http://m.i7wx.net/read/5704_1_1.html", "xhdtsgs.rss"],
             ["人道大圣", "http://m.i7wx.net/read/603015_1_1.html", "rdds.rss"]]


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
        if tags == 'ul':
            for (name, value) in attrs:
                if name == 'class' and value == 'chapters':
                    self.inRightTags = True
        if self.inRightTags and tags == 'a':
            for (name, value) in attrs:
                if name == 'href':
                    self.chapterLink = value

    def handle_endtag(self, tags):
        if tags == 'ul':
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
        self.inRightTags = False
        self.isContent = False

    def handle_starttag(self, tags, attrs):
        if tags == 'div':
            for (name, value) in attrs:
                if name == 'id' and value == 'novelcontent':
                    self.inRightTags = True
        if self.inRightTags and tags == 'p':
            self.isContent = True
        if tags == 'a':
            for (name, value) in attrs:
                if name == 'href':
                    self.currentLink = value

    def handle_endtag(self, tags):
        if self.isContent and tags == 'p':
            self.inRightTags = False
            self.isContent = False

    def handle_data(self, data):
        if self.isContent:
            self.content += str(data).strip() + '</br>'
            self.next = ''
        elif '下一页' == data:
            self.next = 'http://m.i7wx.net' + self.currentLink


def parse(history_path='./'):
    chapters_parser = ChaptersHTMLParser()
    content_parser = ContentHTMLParser()
    for book in BOOK_LIST:
        rss_feed = RSSFeed(book[0], '')
        if os.path.exists(history_path + book[2]):
            rss_feed.load(history_path + book[2])
        response = requests.get(book[1])
        html = response.text
        chapters_parser.feed(html)
        for chapter in chapters_parser.chapters[0:5]:
            if rss_feed.exist(chapter['name']) is False:
                content_parser.next = chapter['link']
                content_parser.content = ''
                while content_parser.next != '':
                    response = requests.get(content_parser.next)
                    html = response.text
                    content_parser.feed(html)
                rss_feed.add_item(chapter['name'],
                                  content_parser.content.replace('本章未完，请点击下一页继续阅读》》', ''),
                                  chapter['link'])
                push_wechat_message('# {} - {}'.format(book[0], chapter['name']), link=chapter['link'])

        rss_feed.save(history_path + book[2])


if __name__ == '__main__':
    parse('../rss/')

