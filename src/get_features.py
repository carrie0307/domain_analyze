# -*- coding: UTF-8 -*-
import MySQLdb
import basic_map


class Domain_features():
    def __init__(self, domain):
        self.domain = domain
        self.ID = hash(domain)
        self.con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys")
        self.cur = self.con.cursor()


    def get_whois_features(self):
        '''
        从whois表读取顶级域、注册邮箱类型和注册商，并根据Basic_map转化为数字标签
        '''
        SQL = "SELECT tld, RIGHT(reg_email, LENGTH(reg_email)-instr(reg_email,'@')), sponsoring_registrar FROM whois WHERE ID = %s" %(self.ID)
        self.cur.execute(SQL)
        res = self.cur.fetchone()
        print res
        if str(res[0]) in basic_map.tld_Map.keys():
            tld = basic_map.tld_Map[str(res[0])] # 将顶级域转化为对应的数字标签
        else:
            tld = basic_map.tld_Map['other']
        if str(res[1]) in basic_map.email_Map.keys():
            reg_email = basic_map.email_Map[(str(res[1]))]
        else:
            reg_email = basic_map.email_Map['other']
        if str(res[2]) in basic_map.spon_registrar_Map.keys():
            spon = basic_map.spon_registrar_Map[str(res[2])]
        else:
            spon = basic_map.spon_registrar_Map['other']
        return [tld, reg_email, spon]


    def get_malicious_info_feature(self):
        '''
        从malicious_info表读取是否包含恶意关键词和HTTPcode，并根据Basic_map转化为数字标签
        '''
        SQL = "SELECT RIGHT(flag,1), HTTPcode FROM malicious_info WHERE ID = %s" %(self.ID)
        self.cur.execute(SQL)
        res = self.cur.fetchone()
        keyword_feature = basic_map.keyword_Map[str(res[0])]
        HTTPcode_feature = basic_map.Httpcode_Map(int(res[1]))
        return [keyword_feature, HTTPcode_feature]

    def get_locate_feature(self):
        '''
        从locate表读取是否包含地理位置一致性比结果，并根据Basic_map转化为数字标签
        '''
        SQL = "SELECT cmp FROM locate WHERE ID = %s" %(self.ID)
        self.cur.execute(SQL)
        res = self.cur.fetchone()
        if str(res[0]) in basic_map.cmp_Map.keys():
            cmp = basic_map.cmp_Map[str(res[0])]
        else:
            cmp = basic_map.cmp_Map['other']
        return cmp

    def get_domain_features(self):
        '''
        将以上三个表中读取的结果汇总到features列表中
        '''
        features = self.get_whois_features()
        features.extend(self.get_malicious_info_feature())
        features.append(self.get_locate_feature())
        self.cur.close()
        self.con.close()
        return features


if __name__ == '__main__':
    d = Domain_features("boda19.com")
    print d.get_domain_features()
