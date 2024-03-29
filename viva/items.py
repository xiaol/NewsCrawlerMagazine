# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#class VivaElement(object):

class Magazine(object):
    def __init__(self):
        self.samesort_magid_list = []            # String : 同类文章推荐 id
        self.beforeperiod_magazine_id_list = []  # String : 同期刊 过去文章 id

        self.magazine_desc = ''                  # String : 本期刊文章概要
        self.magazine_period = ''                # String : 本期刊（月/周)

        self.magazine_date = ''                  # String : 期刊发布日期
        self.magazine_channelname = ''           # String : 期刊所属频道
        self.magazine_brandname = ''             # String : 期刊名
        self.magazine_brandid = ''               # String : 期刊id
        self.magazine_img_url = ''               # String : 期刊小图url
        self.magazine_mimg_url = ''              # String : 期刊大图url
        self.magazine_id = ''                    # Int : 期刊杂志唯一标示id

class Channel(object):
    def __init__(self):
        self.channel_id = ""                   # String : 文章频道id
        self.channel_name = ""                 # String :文章频道名


class TopicBlockItem(object):
    def __init__(self):
        self.topic_block_id = ""                        # String : 话题 block id
        self.topic_block_item_id = ""                   # String : 话题item id primary key
        self.topic_block_item_title = ""                # String : 话题item title
        self.topic_block_item_img_url = ""              # String : 话题 小图
        self.topic_block_item_mimg_url = ""             # String : 话题 中图
        self.topic_block_item_bimg_url = ""             # String : 话题 大图
        self.topic_block_item_content = ""              # String : 话题 内容


class TopicBlock(object):
    def __init__(self):
        self.topic_id = ""                        # String :topic id 作为Primary key.
        self.topic_block_id =  ""                 # String : 模块 id
        self.topic_block_item_list = []           # Item List : Block
        #self.magazine_url_list = []               # magazine url list. Not used

class TopicItem(scrapy.Item):
    """
    Hold all the topic items.
    """
    item_type = scrapy.Field()
    topic_channel_id = scrapy.Field()               #
    topic_magid_list = scrapy.Field()               # String : magid list
    topic_id = scrapy.Field()                       # String : 话题 id
    topic_name = scrapy.Field()                     # String : 话题 name
    topic_block_list = scrapy.Field()               # List Block : Block 列表


class ArticleItem(scrapy.Item):
    """
    Hold all the artile item.
    """
    article_id = scrapy.Field()          # Index of the magazine article
    title = scrapy.Field()               # title of the magazine
    item_type = scrapy.Field()           # type to identify this type
    magazine_id = scrapy.Field()         # magazine id
    html = scrapy.Field()                #List [class article]


class MagazineItem(scrapy.Item):
    """
    杂志对象
    """

    item_type = scrapy.Field()

    magazine = scrapy.Field()               # Magazine


class ChannelItem(scrapy.Item):
    """
    频道对象
    """
    item_type = scrapy.Field()

    channel = scrapy.Field()


class VivaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
