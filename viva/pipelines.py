# !/usr/bin/python

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import base64
import sys
import uniout
import requests
import json

#conn_string = "host = '121.40.34.56' dbname = 'posgtes' password = 'LYpg&postgres@zzg' "

es_base_url = "http://source2.deeporiginalx.com:9200/magazine/"

class VivaPipeline(object):
    def process_item(self, item, spider):
        return item

class ArticlePipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):

        print 'In article pipeline '

        try:
            if item is None or item.get('item_type') != 'articles_item':
                return item
        except Exception ,e :
            print e

        es_magazine_article_url = es_base_url + 'article/'
        article_list = item.get('article_list')

        # Construct article one by one from the magazine period, and insert into elasticsearch via post http request.
        for article in article_list:
            temp_dict = {}

            temp_dict.setdefault('title', article.title)
            temp_dict.setdafault('magazine_id',article.magid)

            temp_dict.setdefault('headline', article.headline_list)
            temp_dict.setdefault('content', article.content_section_list)
            temp_dict.setdefault('img_url_list', article.url_picture_list)

            print 'article :'

            json_data = json.dumps(temp_dict, ensure_ascii = False)
            try:
                ret = requests.post(es_magazine_article_url, json_data)
            except Exception, e:
                print e

class MagazinePipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        print 'In magazine pipeline'


        try:
            if item is None or item.get('item_type') != 'magazine_item':
                return item
        except Exception, e:
            return

        es_magazine_desc_url = es_base_url + 'magazine_desc/'

        magazine = item.get('magazine')
        temp_dict = {}

        temp_dict.setdefault('date', magazine.magazine_date)
        temp_dict.setdefault('period', magazine.magazine_period)
        temp_dict.setdefault('img_url', magazine.magazine_img_url)
        temp_dict.setdefault('channel_name', magazine.magazine_channelname)
        temp_dict.setdefault('brand_name', magazine.magazine_brandname)
        temp_dict.setdefault('brand_id', magazine.magazine_brandname)
        temp_dict.setdefault('magazine_desc', magazine.magazine_desc)
        temp_dict.setdefault('samesort_magid_list', magazine.samesort_magid_list)
        temp_dict.setdefault('before_period_magid_list', magazine.beforeperiod_magazine_id_list)

        print temp_dict
        json_data = json.dumps(temp_dict, ensure_ascii = False)
        ret = requests.post(es_magazine_desc_url, json_data)
        print ret.content

class ChannelPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        print 'In channel pipeline'

        es_magazine_channel_url = es_base_url + 'channel/'
        try:
            if item is None or item.get('item_type') != 'channel_item' :
                return item
        except Exception ,e :
            print e
        channel = item.get('channel')

        temp_dict = {}
        temp_dict.setdefault('channel_name', channel.channel_name)
        temp_dict.setdefault('channel_id', channel.channel_id)

        print temp_dict
        json_data = json.dumps(temp_dict, ensure_ascii = False)
        ret = requests.post(es_magazine_channel_url, json_data)
        print ret

class TopicPipeline(object):
    def process_item(self, item, spider):

        print 'In topic pipeline'
        try:
            if item is None or item.get("item_type") != 'topic_item':
                return item
        except Exception, e:
            print e
        es_magazine_topic_url = es_base_url + 'topic/'

        temp_dict ={}
        temp_dict.setdefault('topic_name', item.get("topic_name"))
        temp_dict.setdefault('topic_id', item.get('topic_id'))
        temp_dict.setdefault('topic_channel_id', item.get('topic_channel_id'))

        json_data = json.dumps(temp_dict, ensure_ascii = False)
        ret = requests.post(es_magazine_topic_url, json_data)

        print ret
        topic_block_list = item.get('topic_block_list')

        es_magazine_topic_block_url = es_base_url +'topic_block_desc/'
        for topic_block in topic_block_list:
            temp_dict = {}
            temp_dict.setdefault('topic_id', topic_block.topic_id)
            temp_dict.setdefault('topic_block_id', topic_block.topic_block_id)
            #temp_dict.setdefault('magazine_url_list', topic_block.url)

            topic_block_item_list = topic_block.topic_block_item_list
            json_data = json.dumps(temp_dict, ensure_ascii = False)
            ret = requests.post(es_magazine_topic_block_url, json_data)

            es_magazine_topic_block_item_url = es_base_url +'topic_block_item/'
            for topic_block_item in topic_block_item_list:

                temp_dict = {}
                temp_dict.setdefault('topic_block_item_id', topic_block_item.topic_block_item_id)
                temp_dict.setdefault('topic_block_item_title', topic_block_item.topic_block_item_title)
                temp_dict.setdefault('topic_block_item_content', topic_block_item.topic_block_item_content)

                json_data = json.dumps(temp_dict, ensure_ascii = False)
                ret = requests.post(es_magazine_topic_block_item_url, json_data)
                print ret