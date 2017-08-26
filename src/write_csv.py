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

abnormal_domains = ['agherhaerf.ga','interlei.gr','icloud-iphnoe.ren',
'd8.cm','raenqt.ga','apple-iphnoe-myapp.ren',
'gyivz.ren','0635jia.com','id-apple.asia',
'4399.cm','apple-ic-icluod.ren','cloudns.asia',
'apple-id.asia','163.cm','yh.cm','ccbycc.pw','icloud-apple-ip.ren',
'apple-app.ren','netgate.co.za','yhvfyjhguijf.ga','apple-iphnoe-icloud.ren']

con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys")
cur=con.cursor()

def get_domain():
    global features_dict
    SQL = "SELECT ID, domain FROM domain_index WHERE ID IN (%s)" %(basicID_set)
    cur.execute(SQL)
    result = cur.fetchall()
    for item in result:
        features_dict[int(item[0])] = [item[1]]



def get_whois_info():
    global features_dict
    SQL = "SELECT ID, tld, RIGHT(reg_email, LENGTH(reg_email)-instr(reg_email,'@')), sponsoring_registrar FROM whois WHERE ID IN (%s)" %(basicID_set)
    cur.execute(SQL)
    result = cur.fetchall()
    for item in result:
        if str(item[1]) in basic_map.tld_Map.keys():
            tld = basic_map.tld_Map[str(item[1])]
        else:
            tld = basic_map.tld_Map['other']
        if str(item[2]) in basic_map.email_Map.keys():
            reg_email = basic_map.email_Map[str(item[2])]
        else:
            reg_email = basic_map.email_Map['other']
        if str(item[3]) in basic_map.spon_registrar_Map.keys():
            spon_reg = basic_map.spon_registrar_Map[str(item[3])]
        else:
            spon_reg = basic_map.spon_registrar_Map['other']
        features_dict[int(item[0])].extend([tld, reg_email, spon_reg])
    print 'whois got ...\n'


def get_malicious__info():
    '''
    关键词标志与HTTPcode
    '''
    global features_dict
    SQL = "SELECT ID, RIGHT(flag, 1),HTTPcode FROM malicious_info WHERE ID IN (%s)" %(basicID_set)
    cur.execute(SQL)
    result = cur.fetchall()
    for item in result:
        keyword_info = basic_map.keyword_Map[str(item[1])]
        HTTPcode = basic_map.Httpcode_Map(int(item[2]))
        features_dict[int(item[0])].extend([keyword_info, HTTPcode])
    print 'keywords got ...\n'


def get_locateCMP_info():
    global features_dict
    SQL = "SELECT ID, cmp from locate WHERE ID IN (%s)" %(basicID_set)
    cur.execute(SQL)
    result = cur.fetchall()
    for item in result:
        if str(item[1]) in basic_map.cmp_Map.keys():
            cmp = basic_map.cmp_Map[str(item[1])]
        else:
            cmp = basic_map.cmp_Map['other']
        # if int(item[1]) >= 0:
        #     cmp = 1
        # else:
        #     cmp = 2
        features_dict[int(item[0])].extend([cmp])
    print 'locate got ... \n'




def get_web_flag_result():
    global features_dict
    SQL = "SELECT ID, web_judge_result FROM other_info WHERE ID IN (%s)" %(basicID_set)
    cur.execute(SQL)
    result = cur.fetchall()
    for item in result:
        if int(item[1]) == 1:
            judge = 'yes'
        else: # 权威检测恶意的全部用2代替
            judge = 'no'
        features_dict[int(item[0])].extend([judge])
    print 'flag got ...\n'


def write_csv_file(filename):
    f=open(filename,'w')
    w=csv.writer(f)
    w.writerow(['domain','tld','email_type','spon_registrar','keyword', 'httpcode', 'locate_cmp', 'web_judge_result'])
    for key in features_dict.keys():
        if features_dict[key][0] not in abnormal_domains:
            w.writerow(features_dict[key])
    f.close()
    print '完成文件。。。\n'




if __name__ == '__main__':
    get_domain()
    get_whois_info()
    get_malicious__info()
    get_locateCMP_info()
    get_web_flag_result()
    cur.close()
    con.close()
    write_csv_file('../data/dataset-http-cmp-more.csv')
