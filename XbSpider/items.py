# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst

from XbSpider.settings import SQL_DATE_FORMAT
from XbSpider.utils.common import strptime


def date_convert(value):
    return strptime(value, SQL_DATE_FORMAT)

##############################################################################################################

class XbspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CustomItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()

class HospitalProcurementItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    createTime = scrapy.Field(
        input_processor=MapCompose(date_convert)
    )
    originalUrl = scrapy.Field()
    cityId = scrapy.Field()
    cityName = scrapy.Field()
    hospitalId = scrapy.Field()
    hospitalName = scrapy.Field()
    status = scrapy.Field()
    type = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into massage_hospital_procurement(id, title, content, createTime, originalUrl, cityId, cityName, hospitalId, hospitalName, `status`, `type`) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            self["id"],
            self["title"],
            self["content"],
            self["createTime"],
            self["originalUrl"],
            self["cityId"],
            self["cityName"],
            self["hospitalId"],
            self["hospitalName"],
            self["status"],
            self["type"]
        )
        return insert_sql, params