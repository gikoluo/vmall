import scrapy
from . import product_spider

class FruitSpider(product_spider.ProductSpider):
    name = "fruit"

    start_urls = ['http://www.cnhnb.com/p/sgzw/']
