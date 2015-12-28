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

conn_string = "host = '121.40.34.56' dbname = 'posgtes' password = 'LYpg&postgres@zzg' "

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
            
        article_list = item.get('article_list')
        print 'article :'
        for article in article_list:

            print 'title : ' + '\t magid :'

            print article.title + '\t' + article.magid
            print 10 * '-'

            print 'content :'
            print len(article.content_section_list)
            for content in article.content_section_list:
                print content
            print 10 *'-'

            print 'headline :'
            print len(article.headline_list)
            for headline in article.headline_list:
                print headline
            print 10 * '-'

            print 'img_url: '
            for img_url in article.url_picture_list:
                print img_url


class MagazinePipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        print 'In magazine pipeline'
        try:
            if item is None or item.get('item_type') != 'magazine_item':
                return item
        except Exception, e:
            print e
        magazine = item.get('magazine')
        print magazine.magazine_brandname
        print magazine.magazine_desc

class ChannelPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        print 'In channel pipeline'
        try:
            if item is None or item.get('item_type') != 'channel_item' :
                return item
        except Exception ,e :
            print e
        channel = item.get('channel')
        print channel.channel_name
        print channel.channel_id

class TopicPipeline(object):
    def process_item(self, item, spider):


        print 'In topic pipeline'
        try:
            if item is None or item.get("item_type") != 'topic_item':
                return item
        except Exception, e:
            print e

        print 'topic_name :'
        print item.get("topic_name")

        print 'topic_channel_id :'
        print item.get('topic_channel_id')
        print 'topic_id :'
        print item.get("topic_id")

        print 'topic block list length'
        topic_block_list = item.get('topic_block_list')
        print len(topic_block_list)

        for topic_block in topic_block_list:

            topic_block_item_list = topic_block.topic_block_item_list
            print 'block id'
            print topic_block.topic_block_id

            for topic_block_item in topic_block_item_list:
                print 'topic block item id :'
                print topic_block_item.topic_block_item_id
                print 'topic block item title :'
                print topic_block_item.topic_block_item_title
                print 'topic_block_item content :'
                print topic_block_item.topic_block_item_content

