# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class PtiSpider(scrapy.Spider):
    name = 'pti'
    allowed_domains = ['www.ptinews.com/pressrelease/$press']
    script = """
        function main(splash, args)
            splash:set_user_agent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36")
            splash.private_mode_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(1))
            splash:set_viewport_full()
            return splash:html()
        end
    """

    def start_requests(self):
        yield SplashRequest(url='http://www.ptinews.com/pressrelease/$press',
        callback=self.parse,
        endpoint="execute",
        args={
            'lua_source':self.script,
        })
    def parse(self, response):
        table = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdpress"]/table/tbody/tr/td/table/tbody/tr')
        for each in table:
            yield {
                'News Title':each.xpath('.//td[1]/a/text()').get(),
                'Source': each.xpath('.//td[3]/text()').get(),
                'Category':each.xpath('.//td[5]/text()').get(),
                'Date':each.xpath('.//td[7]/text()').get(),
            }
