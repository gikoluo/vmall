import scrapy
import hashlib
from bs4 import BeautifulSoup
from vmall.utils import cleaner




class ProductSpider(scrapy.Spider):
    name = "products"

    # def start_requests(self):
    #     urls = [
    #         'http://www.cnhnb.com/p/sgzw/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # follow links to author pages
        for href in response.css('div.product-contents li a::attr(href)'):
            if '/gongying/' in href.get():
                yield response.follow(href, self.parse_product)

        # follow pagination links
        for a in response.css('div.eye-pager a.number'):
            if len(a.css("::text").get()) == 1:
                href = a.css("::attr(href)").get()
                yield response.follow(href, self.parse)

    def parse_product(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        extract_data = {
            'title': extract_with_css('div.proinfo-title::text'),
            'price': extract_with_css('p.price span.fs30::text'),
            'catalog': response.css('div.breadcrumb a::text')[-2].get().strip(),
            'image': extract_with_css('.magnifier-box img::attr(src)'),
            'description':extract_with_css('.detail-info'),  #cleaner.safe_html()
        }

        data = {
            'ID': hashlib.md5(extract_data['title'].encode()).hexdigest()[0:6],
            '类型': 'simple',
            'SKU': hashlib.md5(extract_data['title'].encode()).hexdigest()[0:6],
            '名称': extract_data['title'],
            '已发布': '1',
            '是推荐产品？': '0',
            '在列表页可见': 'visible',
            '简短描述': '',
            '描述': extract_data['description'],
            #促销开始日期  促销截止日期
            '税状态': 'taxable',
            '税类': '',
            '有货？': '1', 
            '库存': '',
            '库存不足': '',
            '允许缺货下单？': 0,
            '单独出售？': '0',
            #重量(kg) 长度(cm)  宽度 (cm) 高度 (cm)
            #允许顾客评价？ 购物备注    
            '促销价格': extract_data['price'],
            '常规售价': extract_data['price'],
            '分类': extract_data['catalog'],
            '图片': extract_data['image'],
            
            'downloadable': 'no',
            'virtual': 'no',
            'visibility': 'visible',
            'stock':'',
            'stock_status': 'instock',
            'backorders': 'no',
            'manage_stock': 'no',
            'tax_status': 'taxable',
            'weight':'500',
        }

#ID 类型  SKU 名称  已发布 是推荐产品？  在列表页可见  简短描述    描述  促销开始日期  促销截止日期  税状态 税类  有货？ 库存  库存不足    允许缺货下单？ 单独出售？   重量(kg)  长度(cm)  宽度 (cm) 高度 (cm) 允许顾客评价？ 购物备注    促销价格    常规售价    分类  标签  运费类 图片  下载限制    下载的过期天数 父级  分组产品    Upsells 交叉销售    外部链接    按钮文本    位置

        yield data
#ID  类型  SKU 名称  已发布 是推荐产品？  在列表页可见  简短描述    描述  促销开始日期  促销截止日期  税状态 税类  有货？ 库存  库存不足    允许缺货下单？ 单独出售？   重量(kg)  长度(cm)  宽度 (cm) 高度 (cm) 允许顾客评价？ 购物备注    促销价格    常规售价    分类  标签  运费类 图片  下载限制    下载的过期天数 父级  分组产品    Upsells 交叉销售    外部链接    按钮文本    位置
#post_title 
#post_name   
#post_status sku downloadable    
#virtual visibility  stock   stock_status    backorders  manage_stock    regular_price   sale_price  weight  length  width   height  tax_status  tax_class   tax:product_type    tax:product_cat tax:product_tag tax:product_brand   attribute:Color attribute_data:Color    attribute:Size  attribute_data:Size
