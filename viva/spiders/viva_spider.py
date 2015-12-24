#!/usr/bin/env python
# -*- coding:utf-8 -*-

import scrapy
from scrapy import Request

from lxml import etree
import xml.etree.ElementTree as ET
import uniout
from StringIO import StringIO
import urllib2

import re
import time
import sys
print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

print sys.getdefaultencoding()

from viva.items import Article
from viva.items import Magazine

class VivaSpider(scrapy.spiders.Spider):
    name = 'viva'

    vmagid_set = set()
    #start_urls = [
    #        "http://interface.vivame.cn/DataService/interface/login4.jsp?mid=05cee906b27e34c38049a12eeb6125c3&installversion=5.0.2&apn=WIFI&isNewUser=false&clientversion=ZWDJA2480800100&uid=62037942&sid=8118510330804557&installversion=5.0.2&platform=android&appName=ChangDuAndroid&device=smartisan%20YQ601&display=1920x1080x3.0&os=Android4.4.4&ua=KTU84P%20dev-keys"
    #        ]
    start_urls = [
            "http://interface.vivame.cn/DataService/interface/login4.jsp?uid=62034360&platform=iphone&clientversion=VIVAI3320480100&device=iPhone%20OS&display=640*1136&os=9.2&installversion=5.1.1&appName=ChangDuIOS&apn=wifi&mid=91509b6cef8db90c9ab4506246ac73c4&isNewUser=false"
            ]
    url_head_str = 'http://interface.vivame.cn/DataService/interface/'

    #url_category_tail_str = '&dataversion=0&clientversion=ZWDJA2480800100&uid=62037942&sid=0374665634984103&installversion=5.0.2&platform=android&appName=ChangDuAndroid&device=smartisan%20YQ601&display=1920x1080x3.0&os=Android4.4.4&ua=KTU84P%20dev-keys'
    
    url_category_tail_str = '&uid=62034360&clientversion=VIVAI3320480100&pid=zhuanqu&width=640&height=1136&device=iPhone%20OS&display=640*1136&os=9.2&topicid=0&blockid=0&source=node&installversion=5.1.1&appName=ChangDuIOS&sid=8699468962456521'
    
    #One magazine has many articles. action = 0, we can get the whole magazine url
    #url_magazine_head_str = "http://interface.vivame.cn/DataService/interface/iphone_getMagazine.jsp?vmagid="
    url_magazine_head_str = "http://interface.vivame.cn/DataService/interface/iphone_getView.jsp?vmagid="

    url_magazine_tail_str = "&uid=62034360&clientversion=VIVAI3320480100&pid=zhuanqu&width=640&height=1136&device=iPhone%20OS&display=640*1136&os=9.2&topicid=0&blockid=0&source=node&installversion=5.1.1&appName=ChangDuIOS&sid=8699468962456521"

    # one topic action = 6
    url_topic_head_str =  "http://interface.vivame.cn/DataService/interface/getTopicIncludeCool.jsp?topicid="
    url_topic_tail_str = "&dataversion=null&clientversion=ZWDJA2480800100&uid=62037942&sid=0505170305002839&installversion=5.0.2&platform=android&appName=ChangDuAndroid&device=smartisan%20YQ601&display=1920x1080x3.0&os=Android4.4.4&ua=KTU84P%20dev-keys"
    
    # Xuan magazine action = 11
    #url_xuan_head_str = "http://interface.vivame.cn/DataService/interface/iphone_cool_getView.jsp?vmagid="
    #url_xuan_tail_str = "&uid=62034360&clientversion=VIVAI3320480100&pid=zhuanqu&width=640&height=1136&device=iPhone%20OS&display=640*1136&os=9.2&topicid=1207&blockid=2963&source=topic&installversion=5.1.1&appName=ChangDuIOS&sid=1201606787832901"

    # Magazine list action = 13
    url_magazine_list_head_str = "http://interface.vivame.cn/DataService/interface/andrd_getMaglistV2.jsp?brandid="
    url_magazine_list_tail_str = "&pageindex=1&pagesize=6&clientversion=ZWDJA2480800100&sid=0505170305002839&type=0&width=0&height=0&clientversion=ZWDJA2480800100&uid=62037942&sid=0505170305002839&installversion=5.0.2&platform=android&appName=ChangDuAndroid&device=smartisan%20YQ601&display=1920x1080x3.0&os=Android4.4.4&ua=KTU84P%20dev-keys"

    #url_magazine_tail_str = "&clientversion=ZWDJA2480800100&sid=6118079447449811&clientversion=ZWDJA2480800100&uid=62037942&sid=6118079447449811&installversion=5.0.2&platform=android&appName=ChangDuAndroid&device=smartisan%20YQ601&display=1920x1080x3.0&os=Android4.4.4&ua=KTU84P%20dev-ke"

    def valid_id_check(self, vmagid):
        if vmagid in self.vmagid_set:
            return False
        else:
            return True

    def parse(self, response):
        html = response.body

        xml_parser = etree.HTMLParser()
        tree = etree.parse(StringIO(html) , xml_parser)
        topic_nodes_list = tree.xpath('.//block[@name="menu"] [@version="1"]')

        classification_tuple_list = []
        for topic_node in topic_nodes_list[0].getchildren():
            print topic_node.tag, topic_node.attrib
            print 'topic_id :' + topic_node.attrib['topicid']
            print 'category :' + topic_node.attrib['name']

            classification = topic_node.attrib['name']

            print 'url :' + topic_node.attrib['url']
            topic_url = self.url_head_str + topic_node.attrib['url'] + self.url_category_tail_str
            print 'topic_url :' +  topic_url
            classification_tuple_list.append((topic_url, classification))
        
        # Visit all the big caption web cages by the urls we get from last page.
        for tuple_iter in classification_tuple_list:
            category_page = urllib2.urlopen(tuple_iter[0]).read()
            self.category_page_parse(category_page, tuple_iter[1])


    #Parse the toppest line caption web page.
    def category_page_parse(self, category_page , classification):
        category_xml_parser = etree.HTMLParser()
        category_tree = etree.parse(StringIO(category_page), category_xml_parser)
        
        # xml category topic - block - item
        block_node_list = category_tree.xpath('.//block [@id]')
        print block_node_list
        
        magazine_id_list = []
        
        for block_node in block_node_list:
            sub_block_node_list = block_node.xpath('.//item [@id]')

            # Iterate all sub_block to generate next level web page url addresses.
            for sub_block_node in sub_block_node_list:
                if sub_block_node.attrib.has_key('url'):
                    # 标签为 url 的 value 是 vmagid 很重要
                    url_id = sub_block_node.attrib['url']
                    if ':' in url_id:
                        url_id = url_id.split(':')[0]

                # 根据 action 的种类 来判断访问的 url 类型
                #try: 如果action = 0,那么我们获取每一篇杂志的实际内容文件的url,并解析出文章内容及图片地址和相关的杂志的vmagid,再根据此vmagid去不停获取新的杂志文章内容，直到递归完毕,vmagid是全局唯一的，保存在一个全局中，防止重复。
                if sub_block_node.attrib['action'] == '0':
                    print 'action type ' + sub_block_node.attrib['action']
                    magazine_url =  self.url_magazine_head_str + url_id + self.url_magazine_tail_str

                    #判断vmagid 是否被访问过，如果被访问过，那么就continue，否则访问
                    if self.valid_id_check(int(url_id)):
                        magazine_page = urllib2.urlopen(magazine_url).read()
                        self.vmagid_set.add(int(url_id))
                        self.magazine_overview_parser(magazine_page)

                elif sub_block_node.attrib['action'] == '6':
                    continue
                elif sub_block_node.attrib['action'] == '11':
                    continue
                # 如果action = 13，那么我们获取的是杂志的url_list，然后根据其中的vmagid去得到内容，同上。
                else:
                    magazine_list_url = self.url_magazine_list_head_str + url_id + self.url_magazine_list_tail_str
                    try:
                        if self.valid_id_check(int(url_id)):
                            self.vmagid_set.add(int(url_id))
                            magazine_list_webpage = urllib2.urlopen(magazine_list_url).read()
                            self.magazine_list_parser(magazine_list_webpage)
                    except Exception, e:
                        print e
                        pass


    # 得到本杂志所有的期数的vmagid
    def magazine_list_parser(self, magazine_list_page):
        magazine_list_xml_parser = etree.HTMLParser()
        magazine_list_tree = etree.parse(StringIO(magazine_list_page), magazine_list_xml_parser)
        magazine_periods_node_list = magazine_list_tree.xpath('.//maglist/item')


        print 'from magazine list magazine periods ids'
        for magazine_periods_node in magazine_periods_node_list:
            vmgaid =  magazine_periods_node.attrib['vmagid']

            magazine_url = self.url_magazine_head_str + magazine_periods_node.attrib['vmagid'] + self.url_magazine_tail_str
            magazine_page = urllib2.urlopen(magazine_url).read()

            self.magazine_overview_parser(magazine_page)


    # 得到相关杂志或者前期杂志的 id 列表。
    def get_magazine_id_list(self, item_list):
        vmagid_list = []
        for item in item_list:
            vmagid_list.append(item.attrib['vmagid'])
        return vmagid_list

    # 得到本期杂志内容的url，及往期杂志和相似杂志的id, 无论哪种action，最终都要使用这个方法去获取杂志的内容
    def magazine_overview_parser(self, magazine_overview_page):
        magazine_overview_xml_parser = etree.HTMLParser()
        magazine_overview_tree = etree.parse(StringIO(magazine_overview_page), magazine_overview_xml_parser)

        if magazine_overview_tree.xpath('.//card')[0].attrib['result'] == "2000":
            return

        magazine_struct = Magazine

        magazine_info_node = magazine_overview_tree.xpath(".//magazinevx2")[0]

        magazine_struct.magazine_picture_url_list = magazine_info_node
        magazine_struct.magazine_img_url = magazine_info_node.attrib['img']
        magazine_struct.magazine_mimg_url = magazine_info_node.attrib['mimg']
        magazine_struct.magazine_brandid = magazine_info_node.attrib["brandid"]
        magazine_struct.magazine_brandname = magazine_info_node.attrib["brandname"]
        magazine_struct.magazine_channelname = magazine_info_node.attrib['channelname']
        magazine_struct.magazine_date = magazine_info_node.attrib['date']
        magazine_struct.magazine_brandperiod = magazine_info_node.attrib['brandperiod']
        magazine_struct.period =  magazine_info_node.attrib['period']
        magazine_struct.desc = "".join(magazine_overview_tree.xpath(".//briefvx2")[0].itertext())

        #samesort 是指同类期刊 tag。
        samesort_magazine_node_list = magazine_overview_tree.xpath('.//samesort/item')
        magazine_struct.samesort_magid_list = self.get_magazine_id_list(samesort_magazine_node_list)

        print 'samesort_magazine_node_list : '
        print self.get_magazine_id_list(samesort_magazine_node_list)

        # beforeperiod 是往期杂志 tag
        beforeperiod_magazine_node_list = magazine_overview_tree.xpath('.//beforeperiod/item')
        magazine_struct.beforeperiod_magazine_id_list = self.get_magazine_id_list(beforeperiod_magazine_node_list)

        print 'beforeperiod_magazine_node_list :'
        print self.get_magazine_id_list(beforeperiod_magazine_node_list)

        print 100 *'*'
        print magazine_overview_page
        vmagid = magazine_info_node.attrib['vmagid']
        print 'self magazine id :'
        print vmagid

        try:
        # urlvx2 是格式为vx2的 文件格式 url 标签
            magazine_content_url = ''.join(magazine_overview_tree.xpath('.//urlvx2')[0].itertext())

            print "magazine_content_url :"
            print magazine_content_url
        except Exception, e:
            print e
            pass
        magazine_content = urllib2.urlopen(magazine_content_url).read()
        self.magazine_content_parser(magazine_content, vmagid)


        samesort_magazine_node_list = magazine_overview_tree.xpath('.//samesort/item')
        print 'from magazine samesort  ids :'
        for samesort_magazine_node in samesort_magazine_node_list:
            vmagid =  samesort_magazine_node.attrib['vmagid']
            if self.valid_id_check(int(vmagid)):
                self.vmagid_set.add(int(vmagid))
                magazine_url = self.url_magazine_head_str + samesort_magazine_node.attrib['vmagid'] + self.url_magazine_tail_str

                print ' magazine_url :'
                print magazine_url
                magazine_page = urllib2.urlopen(magazine_url).read()
                self.magazine_overview_parser(magazine_page)


        print 'from period_magazine'

        for beforeperiod_magazine_node in beforeperiod_magazine_node_list:
            vmagid = beforeperiod_magazine_node.attrib['vmagid']
            if self.valid_id_check(int(vmagid)):
                self.vmagid_set.add(int(vmagid))
                print ' magazine_url :'

                magazine_url = self.url_magazine_head_str + beforeperiod_magazine_node.attrib['vmagid'] + self.url_magazine_tail_str
                print magazine_url
                magazine_page = urllib2.urlopen(magazine_url).read()
                self.magazine_overview_parser(magazine_page)


    # 用正则表达式去找到所有的html标签内的内容，并获取杂志内各篇文章的文本内容。
    def magazine_content_parser(self, magazine_file , vmagid):

        pattern = "<html>.*?</html>"
        html_section_list = re.findall(pattern, magazine_file.replace("\n", ""))
        category_list = []

        #print html_section_list
        self.get_category_index(html_section_list, category_list)

        print 'category :'
        for category in category_list:
                print category

        # 根据文章标题对 html_section里面的内容进行组合。杂志文章分为不定的篇幅，篇幅张数由tag 和 title 的出现次数有关。
        artile_list = []
        for category_index in category_list:
            article = Article()
            article.title = category_index

            print 'category index :'
            print category_index

            # 获取 包含此 title的html_section的内容，包括图片url和文本内容，获取后删除此html_section
            for html_section in html_section_list:
                html_section_xml_parser = etree.HTMLParser()

                url_magazine_img_str = "http://wap.vivame.cn/mag/"
                url_magazine_img_str += vmagid
                url_magazine_img_str += "/vx2/"


                html_section_tree = etree.parse(StringIO(html_section), html_section_xml_parser)
                if category_index in "".join(html_section_tree.xpath('.//title')[0].itertext()) and \
                        (category_index != '封面' and category_index != '封底'):

                    print html_section

                    headline = ""
                    print 'headline :'
                    # 将headline 包括h1 或者 h2的所有文本获取出来。
                    try:
                        headline = "".join(html_section_tree.xpath('.//div [@class="h1" or @class = "h2"]')[0].itertext())
                        print headline
                    except Exception, e:
                        pass

                    article.head_line = headline

                    content_node_list = html_section_tree.xpath('.//div [@class="text"]//p')
                    content = ""
                    for content_node in content_node_list:
                        content += "".join(content_node.itertext())
                    print 'content: '
                    print content

                    article.content_section_list.append(content)

                    # 抽取出来杂志出来以后，将这个html_section 删除掉。
                    url_magazine_img_node_list = html_section_tree.xpath('.//img')
                    img_node_value = url_magazine_img_node_list[-1].attrib['onclick']
                    url_magazine_img_tail_str = img_node_value.replace("popArticleImage", "").replace("('", "").replace("')", "")
                    url_magazine_img_str += url_magazine_img_tail_str

                    print url_magazine_img_str

                    html_section_list.remove(html_section)


    # 从包含目录的html_section中获取杂志的目录索引 放到 category_list 中。
    def get_category_index(self, html_section_list, category_list):
        for html_section in html_section_list:
            html_section_xml_parser = etree.HTMLParser()
            html_section_tree = etree.parse(StringIO(html_section), html_section_xml_parser)

            if "".join(html_section_tree.xpath('.//title')[0].itertext()) == "目录":

                # 获取所有目录索引节点via etree
                category_index_node_list = html_section_tree.xpath('.//div [@class="block1"]//h2')
                print "category index length : "
                print len(category_index_node_list)
                # 获取所有文字索引
                for category_index_node in category_index_node_list:
                    category_list.append("".join(category_index_node.itertext()))
                # 获取到这个目录html section后，便可以去掉这个section，减少运算
                html_section_list.remove(html_section)
                break
