# -*- coding: UTF-8 -*-
'''
原始特征项转化为数字标签（注意这里的数字不具备大小关系，因此需要在data_processing.py中用pd.get_dummies()函数处理
由于有些特征项内容种类繁杂，因此对top10进行了具体的数字标签，其他用Other代替，而这耶稣进行数字编码的目的之一
'''

tld_Map = {'com':1, 'cn':2, 'cc':3, 'net':4, 'org':5,
        'info':6, 'tv':7, 'me':8, 'biz':9, 'co':10, 'pw': 11,
        'win':12, 'top':13, 'tk':14, 'xyz':15, 'other': 16}

email_Map = {'': 0, 'qq.com':1, '163.com':2, '126.com':3, 'foxmail.com': 4,
            'YinSiBaoHu.AliYun.com':5, 'gmail':6, 'hotmail':7, 'sina.com':8,
            'outlook.com':9, 'privacyprotect.org':10, 'juming.com':11, 'other':12}

spon_registrar_Map = {'':0, 'HICHINA ZHICHENG TECHNOLOGY LTD.':1, 'XINNET TECHNOLOGY CORPORATION':2,
                    'eName Technology Co., Ltd.':3, 'West263 International Limited':4, '阿里云计算有限公司（万网）':5,
                    'Bizcn.com,Inc.':6, '22NET, INC.':7, 'SHANGHAI MEICHENG TECHNOLOGY INFORMATION DEVELOPMENT CO., LTD.':8,
                    'Beijing Innovative Linkage Technology Ltd. dba dns.com.cn':9,
                    'PDR Ltd. d/b/a PublicDomainRegistry.com':10, 'ENOM, INC.':11,'other':12}

keyword_Map = {'8':1, '9':2, '2':3, '1':4, '0':5, '6':5}

cmp_Map = {'-2':1, '22':2, '33':3, '11':4, '21':5, '32':6, '0':7, '31':8, '23':9, '10':10, '44':11, 'other':12}

def Httpcode_Map(num):
    if num >= 300:
        return 1
    elif num >= 0:
        return 2
    elif num == -2:
        return 3
    else:
        return 4
