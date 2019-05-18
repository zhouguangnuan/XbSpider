# -*- coding: utf-8 -*-
from urllib import parse

import requests
import scrapy
from scrapy import Selector, Request

from XbSpider.items import CustomItemLoader, HospitalProcurementItem
from XbSpider.settings import SQL_DATE_FORMAT
from XbSpider.utils.common import get_md5, get_type, find_last_hospital_procurement_item, get_match_result, strptime

session = requests.session()
header = {
    "HOST": "www.ndfsyy.com",
    "Referer": "https://www.ndfsyy.com",
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
}

# 医院信息
cityId = "3302"
cityName = "宁波市"
hospitalId = 25
hospitalName = "宁波大学医学院附属医院"

class Spider_3302_25(scrapy.Spider):
    name = '3302_25'
    allowed_domains = ['www.ndfsyy.com']
    start_urls = ['http://www.ndfsyy.com/']

    def parse(self, response):
        last_hospital_procurement_item = find_last_hospital_procurement_item(cityId, hospitalId)

        # 1. 请求采购招标列表数据
        post_url = "http://www.ndfsyy.com/module/web/jpage/dataproxy.jsp?startrecord=1&endrecord=45&perpage=15"
        post_data = {
            "col": "1",
            "appid": "1",
            "webid": "7",
            "path": "/",
            "columnid": "968",
            "sourceContentType": "1",
            "unitid": "1428",
            "webname": "宁波市宁大附属医院",
            "permissiontype": "0"
        }
        response_text = session.post(post_url, data=post_data, headers=header).text
        response_text = response_text.replace('<![CDATA[', '').replace(']]>', '')

        # 2. 使用 scrapy.selector.Selector 解析 xml
        sel = Selector(text=response_text)

        # 3. 解析采购招标列详情链接地址
        for line in sel.css('a'):
            href = line.css("::attr(href)").extract_first("")
            createTime = line.css(".yyrytm4::text").extract_first("")
            createTime = strptime(createTime, SQL_DATE_FORMAT)

            # 通过日期判断，避免数据重复处理，日期相同时冗余处理，id机制会保证数据库记录不重复
            if last_hospital_procurement_item != None and createTime < last_hospital_procurement_item[1].date():
                break

            yield Request(url=parse.urljoin(response.url, href), callback=self.parse_detail)

    def parse_detail(self, response):
        # 通过item loader加载item
        item_loader = CustomItemLoader(item=HospitalProcurementItem(), response=response)
        item_loader.add_value("cityId", cityId)
        item_loader.add_value("cityName", cityName)
        item_loader.add_value("hospitalId", hospitalId)
        item_loader.add_value("hospitalName", hospitalName)
        item_loader.add_value("status", 0)

        # 各网站个性化爬取规则
        item_loader.add_value("id", get_md5(response.url))
        title = response.css(".rightdiv h2::text").extract()[0]
        item_loader.add_value("title", title)
        item_loader.add_css("content", ".rightdiv div.entry")
        createTime = response.css(".rightdiv .nrshuoming::text").extract_first()
        createTime = get_match_result("[\d]{4}-[\d]{2}-[\d]{2}", createTime, 1)
        item_loader.add_value("createTime", createTime)
        item_loader.add_value("originalUrl", response.url)
        item_loader.add_value("type", get_type(title))

        article_item = item_loader.load_item()
        yield article_item