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

print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

print 'pipeline encoding :'
print sys.getdefaultencoding()
#conn_string = "host = '121.40.34.56' dbname = 'posgtes' password = 'LYpg&postgres@zzg' "

es_base_url = "http://source2.deeporiginalx.com:9200/magazine/"
#pos_host_url = "http://api.deeporiginalx.com/"

class VivaPipeline(object):
    def process_item(self, item, spider):
        return item

class ArticlePipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):

        print 'In article pipeline '

        try:
            if item is None or item.get('item_type') != 'article_item':
                return item
        except Exception ,e :
            print e

        article_url = "bdp/magazine/acticle"
        #pos_host_article_url = pos_host_url + article_url

        es_magazine_article_url = es_base_url + 'article/'
        #article_list = item.get('article_list')

        # Construct article one by one from the magazine period, and insert into elasticsearch via post http request.

        print 'article :'
        temp_dict = {}
        temp_dict['magazine_id'] = item.get('magazine_id')
        html_data  = item.get('html')
        if html_data is None:
            target_url = es_base_url + 'magazine_desc/' + temp_dict['magazine_id'] + '/'
            requests.delete(target_url)
        else:
            temp_dict['title'] = item.get("title").encode('utf-8')
            temp_dict['html'] = html_data
            json_data = json.dumps(temp_dict, ensure_ascii = False)
            print json_data
            ret = requests.post(es_magazine_article_url, json_data)
            print ret


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

        magazine = item.get('magazine')

        #magazine_url = "bdp/magazine/brand"
        #pos_host_magazine_url  = pos_host_url + magazine_url

        #pos_temp_dict = {}
        #pos_temp_dict.setdefault('date', magazine.magazine_date)
        #pos_temp_dict.setdefault('period', magazine.magazine_period)
        #pos_temp_dict.setdefault('img_url', magazine.magazine_img_url)
        #pos_temp_dict.setdefault('channel_name', magazine.magazine_channelname)
        #pos_temp_dict.setdefault('brand_name', magazine.magazine_brandname)
        #pos_temp_dict.setdefault('brand_id', int(magazine.magazine_brandid))
        #pos_temp_dict.setdefault('magazine_desc', magazine.magazine_desc)
        #pos_temp_dict.setdefault('samesort_magid_list', magazine.samesort_magid_list)
        #pos_temp_dict.setdefault('before_period_magid_list', magazine.beforeperiod_magazine_id_list)
        #pos_temp_dict.setdefault('magazine_id', int(magazine.magazine_id))

        #pos_json_data = json.dumps(pos_temp_dict, ensure_ascii=False)
        #pos_ret = requests.post(pos_host_magazine_url, pos_json_data)

        #print pos_ret

        es_magazine_desc_url = es_base_url + 'magazine_desc/' + magazine.magazine_id + '/'
        temp_dict = {}

        temp_dict.setdefault('period', magazine.magazine_period.encode('utf-8'))
        temp_dict.setdefault('date', magazine.magazine_date)
        temp_dict.setdefault('img_url', magazine.magazine_img_url)
        temp_dict.setdefault('channel_name', magazine.magazine_channelname.encode('utf-8'))
        temp_dict.setdefault('brand_name', magazine.magazine_brandname.encode('utf-8'))
        temp_dict.setdefault('brand_id', magazine.magazine_brandid)
        unicode_magazine_desc = magazine.magazine_desc.replace("<![CDATA[", "").replace("]]>", "")
        temp_dict.setdefault('magazine_desc', unicode_magazine_desc.encode('utf-8'))
        temp_dict.setdefault('samesort_magid_list', magazine.samesort_magid_list)
        temp_dict.setdefault('before_period_magid_list', magazine.beforeperiod_magazine_id_list)
        temp_dict.setdefault('magazine_id', magazine.magazine_id)
        #print temp_dict
        json_data = json.dumps(temp_dict, ensure_ascii = False)
        print 'magazine: '
        print json_data
        # We use (http) put method to create index of elasitcsearch.
        ret = requests.put(es_magazine_desc_url, json_data)
        print ret

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


        #pos_temp_dict = {}
        #pos_temp_dict.setdefault('channel_name', channel.channel_name)
        #pos_temp_dict.setdefault('channel_id', int(channel.channel_id))

        channel_url = "bdp/magazine/channel"
        #pos_host_channel_url = pos_host_url + channel_url

        #pos_json_data = json.dumps(pos_temp_dict, ensure_ascii = False)

        #pos_ret = requests.post(pos_host_channel_url, pos_json_data)
        #print pos_ret

        temp_dict = {}
        temp_dict.setdefault('channel_name', channel.channel_name.encode('utf-8'))
        temp_dict.setdefault('channel_id', channel.channel_id)

        #print temp_dict
        json_data = json.dumps(temp_dict, ensure_ascii = False)
        print 'channel :'
        print json_data
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

        topic_url = "bdp/magazine/topic"
        #pos_host_topic_url = pos_host_url + topic_url

        #pos_temp_dict = {}
        #pos_temp_dict.setdefault('topic_name', item.get("topic_name"))
        #pos_temp_dict.setdefault('topic_id', int(item.get('topic_id')))
        #pos_temp_dict.setdefault('topic_channel_id', int(item.get('topic_channel_id')))

        #pos_json_data = json.dumps(pos_temp_dict, ensure_ascii = False)
        #pos_ret = requests.post(pos_host_topic_url, pos_json_data)

        #print pos_ret

        es_magazine_topic_url = es_base_url + 'topic/'
        temp_dict ={}
        temp_dict.setdefault('topic_name', item.get("topic_name").encode('utf-8'))
        temp_dict.setdefault('topic_id', item.get('topic_id'))
        temp_dict.setdefault('topic_channel_id', item.get('topic_channel_id'))

        json_data = json.dumps(temp_dict, ensure_ascii = False)
        print 'topic :'
        print json_data

        ret = requests.post(es_magazine_topic_url, json_data)

        #print ret
        topic_block_list = item.get('topic_block_list')

        #pos_host_block_url = pos_host_url + 'bdp/magazine/block'
        es_magazine_topic_block_url = es_base_url +'topic_block_desc/'

        for topic_block in topic_block_list:

            #pos_temp_dict = {}
            #pos_temp_dict.setdefault('topic_id', int(topic_block.topic_id))
            #pos_temp_dict.setdefault('topic_block_id', int(topic_block.topic_block_id))
            #pos_json_data = json.dumps(pos_temp_dict, ensure_ascii = False)
            #print pos_json_data
            #pos_ret = requests.post(pos_host_block_url, pos_json_data)

            temp_dict = {}
            temp_dict.setdefault('topic_id', topic_block.topic_id)
            temp_dict.setdefault('topic_block_id', topic_block.topic_block_id)

            topic_block_item_list = topic_block.topic_block_item_list
            json_data = json.dumps(temp_dict, ensure_ascii = False)
            print 'topic block :'
            print json_data
            #ret = requests.post(es_magazine_topic_block_url, json_data)

            es_magazine_topic_block_item_url = es_base_url +'topic_block_item/'
            #pos_host_block_item_url = pos_host_url + "bdp/magazine/item"

            for topic_block_item in topic_block_item_list:
                #pos_temp_dict = {}

                #pos_temp_dict.setdefault('topic_block_id', int(topic_block_item.topic_block_id))
                #pos_temp_dict.setdefault('topic_block_item_id', int(topic_block_item.topic_block_item_id))
                #pos_temp_dict.setdefault('topic_block_item_title', topic_block_item.topic_block_item_title)
                #pos_temp_dict.setdefault('topic_block_item_content', topic_block_item.topic_block_item_content)
                #pos_temp_dict.setdefault('topic_block_item_img_url', topic_block_item.topic_block_item_img_url)
                #pos_temp_dict.setdefault('topic_block_item_mimg_url', topic_block_item.topic_block_item_mimg_url)
                #pos_temp_dict.setdefault('topic_block_item_bimg_url', topic_block_item.topic_block_item_bimg_url)

                #pos_json_data = json.dumps(pos_temp_dict, ensure_ascii = False)
                #print pos_json_data

                #pos_ret = requests.post(pos_host_block_item_url, pos_json_data)

                temp_dict = {}

                temp_dict.setdefault('topic_block_id', topic_block_item.topic_block_id)
                temp_dict.setdefault('topic_block_item_id', topic_block_item.topic_block_item_id)
                temp_dict.setdefault('topic_block_item_title', topic_block_item.topic_block_item_title.encode('utf-8'))
                unicode_topic_block_item_desc = topic_block_item.topic_block_item_content
                temp_dict.setdefault('topic_block_item_content', unicode_topic_block_item_desc.encode('utf-8'))
                temp_dict.setdefault('topic_block_item_img_url', topic_block_item.topic_block_item_img_url)
                temp_dict.setdefault('topic_block_item_mimg_url', topic_block_item.topic_block_item_mimg_url)
                temp_dict.setdefault('topic_block_item_bimg_url', topic_block_item.topic_block_item_bimg_url)

                json_data = json.dumps(temp_dict, ensure_ascii = False)
                print 'topic block item :'
                print json_data
                ret = requests.post(es_magazine_topic_block_item_url, json_data)
                #print ret