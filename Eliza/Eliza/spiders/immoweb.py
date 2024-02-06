import scrapy


class ImmowebSpider(scrapy.Spider):
    name = "immoweb"
    allowed_domains = ["www.immoweb.be"]
    start_urls = ["https://www.immoweb.be/fr/annonce/maison/a-vendre/ixelles/1050/11075842"]

    def parse(self, response):
        pass
