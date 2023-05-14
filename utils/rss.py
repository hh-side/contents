import simplexml
from datetime import datetime


class RSSFeed:
    def __init__(self, title, description):
        self._data = {"rss": {"channel": {
            "title": title,
            "description": description,
            "item": []
        }}}
        self._titles = []

    def load(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            json_xml = simplexml.loads(f.read())
            self._data['rss']['channel']['item'] = json_xml['rss']['channel']['item']
        for item in self._data['rss']['channel']['item']:
            self._titles.append(item['title'])

    def save(self, file_path):
        if len(self._data['rss']['channel']['item']) > 20:
            self._data['rss']['channel']['item'] = self._data['channel']['item'][0:20]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(simplexml.dumps(self._data))

    def exist(self, title):
        return self._titles.__contains__(title)

    def dumps(self):
        return simplexml.dumps(self._data)

    def add_item(self, title, description, link=None):
        if title not in self._titles:
            self._titles.append(title)
            self._data['rss']['channel']['item'].insert(0, {
                "title": title,
                "link": link if link is not None else f'#title={title}',
                "description": description,
                "publish_date": datetime..utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
            })


if __name__ == '__main__':
    rss_feed = RSSFeed('测试', 'Desc')
    rss_feed.add_item("first", "first 那你呢")
    rss_feed.add_item("first——1", "first 111那你呢")
    rss_feed.add_item("first——2", "first 222那你呢")
    rss_feed.add_item("first", "first ？？？？？那你呢")
    print(rss_feed.dumps())
