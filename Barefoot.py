"""This Crawler gets data from Barefootholiday website"""
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
import MySQLdb
class Barefoot(BaseSpider):
    """Starts name of the Crawler here"""
    name = "Barefoot"
    start_urls = ['http://barefootholiday.com/holiday-packages/']
    def __init__(self):
        """Connecting to Database"""
        self.conn = MySQLdb.connect(
            host="localhost", user="root", passwd='01491a0237db',
            db="Barefootdb", charset='utf8', use_unicode=True)
        self.cur = self.conn.cursor()
    def parse(self, response):
        """Nodes starts here"""
        sel = Selector(response)
        nodes = sel.xpath(
            '//div[@class="featured-packages"]/div[@class="row"]/div[@class="col-sm-6"]')
        for node in nodes:
            title = "".join(node.xpath(
                './/div[@class="layer"]/div[@class="heading"]/text()').extract())
            package = "".join(node.xpath(
                './/div[@class="layer"]/div[@class="sub-heading"]/text()').extract())
            descr = "".join(node.xpath('.//div[@class="description"]/p/text()').extract())
            price = "".join(node.xpath(
                './/div[@class="layer"]//div[@class="pricing"]/div[@class="text"]/text()').extract())
            image = "".join(node.xpath('.//div[@class="image"]/img/@src').extract())
            qry = 'insert into bare(title, package, descr, price, image)values(%s, %s, %s, %s, %s)'
            values = (title, package, descr, price, image)
            print qry%values
            self.cur.execute(qry, values)
            self.conn.commit()
