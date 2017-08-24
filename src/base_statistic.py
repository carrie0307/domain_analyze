# -*- coding: UTF-8 -*-
import MySQLdb


con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys")
cur=con.cursor()

def whois_intact_statistic():
    res = {'benign':0, 'malicious': 0}
    SQL = "SELECT whois_flag, COUNT(*) FROM domain_index WHERE ID IN (SELECT ID FROM other_info WHERE web_judge_result = 1) GROUP BY whois_flag"
    cur.execute(SQL)
    result=cur.fetchall()
    print result
    # res['benign'] = int(result[0][0])
    # SQL = "SELECT COUNT(*) FROM domain_index WHERE whois_flag != 1 AND ID IN (SELECT ID FROM other_info WHERE web_judge_result = 2 OR web_judge_flag = 3)"
    # res['malicious'] = int(result[0][0])
    # print res


def tld_statistic():
    res = {'benign':{}, 'malicious': {}}
    SQL = "SELECT tld, COUNT(*) num FROM whois WHERE ID IN (SELECT ID FROM other_info WHERE web_judge_result = 1) GROUP BY tld  ORDER BY num DESC"
    cur.execute(SQL)
    result=cur.fetchall()
    print result
    SQL = "SELECT tld, COUNT(*) num FROM whois WHERE ID IN (SELECT ID FROM other_info WHERE web_judge_result = 2 OR web_judge_result = 3) GROUP BY tld  ORDER BY num DESC"
    cur.execute(SQL)
    result = cur.fetchall()
    print result








if __name__ == '__main__':
    # whois_intact_statistic()
    tld_statistic()
    cur.close()
    con.close()
