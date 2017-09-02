# -*- coding: UTF-8 -*-
'''
获取Alex.cn前100合计2000个域名
'''
import MySQLdb
import requests
from lxml import etree

def get_domains_fromAlex():
    '''
    爬取域名数据
    '''
    domains = []
    for i in range(1,101): #爬取前一百页2000个域名
        url = 'http://www.alexa.cn/siterank/{page}'.format(page = str(i))
        html = requests.get(url).text
        html = etree.HTML(html)
        temp_domains = html.xpath('//*[@class="domain"]/a/text()')
        print temp_domains
        print '\n'
        domains.extend(temp_domains)
    return domains


def insert_domains(domains):
    '''
    将爬取的域名存入domain_index,且设置source = '103'
    '''
    conn = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys")
    cur=conn.cursor()
    cur.execute("select ID from domain_index")
    res = cur.fetchall()
    exist_list = []
    for ID in res:
        exist_list.append(int(ID[0]))
    for domain in domains:
        if ord(domain[0]) >=65 and ord(domain[0])<=90:
            domain = chr(ord(domain[0]) + 32) + domain[1:]
        ID = hash(domain)
        print ID,domain
        if ID not in exist_list:
            sqlstr = "INSERT INTO domain_index(ID,domain,source) VALUES(%s,'%s', '%s')" %(ID,domain,'103')
        else:
            sqlstr = "UPDATE domain_index SET source = '%s' WHERE ID = %s" %('103', ID)
        # print sqlstr + '\n'
        try:
            cur.execute(sqlstr)
        except:
            print ID
        conn.commit()
    cur.close()
    conn.close()
    print 'save over ...'

if __name__ == '__main__':
    domains = get_domains_fromAlex()
    insert_domains(domains)
