# -*- coding: UTF-8 -*-
'''
从站长工具网站排名列表读取网站，获取域名
（未运行）
'''
import urllib2
from lxml import etree
import re
from tld import get_tld

# html = urllib2.urlopen('http://search.top.chinaz.com/top.aspx?p=3&t=all&sort=1').read()
# html = etree.HTML(html)
# ini_urls = html.xpath('//*[@class="w320 PCop"]/a/@href')
# ini_url = html.xpath('//*[@class="w320 PCop"]/a/@href')[0]
ini_url = 'http://top.chinaz.com/Html/site_tms56.com.html'
hostname = re.compile(r'http://top\.chinaz\.com/Html/site_(.+?)\.html').findall(ini_url)
print hostname
