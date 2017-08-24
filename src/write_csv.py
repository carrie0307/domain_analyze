# -*- coding: UTF-8 -*-
import csv
import MySQLdb
import basic_map
'''
    从数据库读取特征项，根据basic_map处理后写成csv文件
'''

# 存储特征项的字典，以ID为key，value内容wei[domain,tld,email_type,spon_registrar,keyword,locate_cmp, web_judge_result]
features_dict = {}

# 选取有权威监测结果的域名作为训练集合
basicID_set = "SELECT ID FROM other_info WHERE web_judge_result = 2 OR web_judge_result = 3 OR web_judge_result = 1"

con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys")
cur=con.cursor()

def get_domain():
    global features_dict
    SQL = "SELECT ID, domain FROM domain_index WHERE ID IN (%s) LIMIT 10" %(basicID_set)
    cur.execute(SQL)
    result = cur.fetchall()
    for item in result:
        features_dict[int(item[0])] = [item[1]]



def get_whois_info():
    global features_dict
    SQL = "SELECT ID, tld, reg_email, sponsoring_registrar FROM whois WHERE ID IN (%s) LIMIT 10" %(basicID_set)
    cur.execute(SQL)
    result = cur.fetchall()
    for item in result:
        features_dict[int(item[0])].extend([item[1], item[2], item[3]])



if __name__ == '__main__':
    get_domain()
    print '=====\n'
    get_whois_info()
    cur.close()
    con.close()
