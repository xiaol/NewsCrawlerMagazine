# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item

#class VivaElement(object):

class Magazine(object):
    samesort_magid_list = []
    beforeperiod_magazine_id_list = []

    magazine_desc = ''
    magazine_period = ''
    magazine_brandperiod = ''
    magazine_date = ''
    magazine_channelname = ''
    magazine_brandname = ''
    magazine_brandid = ''
    magazine_img_url = ''
    magazine_mimg_url = ''

class Article(object):
    title = ""
    headline = []
    content_section_list = []
    url_picture_list = []


class VivaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
