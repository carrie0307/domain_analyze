# -*- coding: UTF-8 -*-
'''
    获取HTTPcode数据
'''
import urllib2
import threading
import Queue
import MySQLdb
import time

domain_q = Queue.Queue()
res_q = Queue.Queue()
counter = 0
thread_num = 20

def get_domains():
    global domain_q
    con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys")
    cur=con.cursor()
    SQL = "SELECT ID,domain FROM domain_index WHERE ID IN (select ID from malicious_info where flag like '%1' or flag like'%2') limit 100"
    cur.execute(SQL)
    result = cur.fetchall()
    cur.close()
    con.close()
    for item in result:
        domain_q.put([item[0], item[1]])


def get_Httpcode():
    global domain_q
    global res_q
    while True:
        if domain_q.empty():
            break
        ID, domain = domain_q.get()
        url = 'http://' + domain
        try:
            response = urllib2.urlopen(url, timeout=2)
            res_q.put([ID, response.code])
        except urllib2.HTTPError, e:
            res_q.put([ID, e.code])
        except urllib2.URLError, e:
            print e.reason
            if str(e.reason) == 'timed out':
                res_q.put([ID, -2])
            else:
                res_q.put([ID, -3])
        except:
            res_q.put([ID, -4]) # -4表示请求有误
    print "get code over ...\n"


def save_Httpcode():
    print 'saving ...'
    global res_q
    global counter
    con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys")
    cur=con.cursor()
    while True:
        ID, code = res_q.get(timeout=60)
        SQL = 'UPDATE malicious_info SET HTTPcode = %s WHERE ID = %s' %(code,ID)
        print SQL + "\n"
        cur.execute(SQL)
        counter = counter + 1
        print 'counter :' + str(counter) + '\n'
        if counter == 100:
            con.commit()
            counter = 0
            print 'Commit ...\n'
    con.commit()
    print 'save over ...\n'
    cur.close()
    con.close()


def main():
    get_domains()
    get_Httpcode_td = []
    for _ in range(thread_num):
        get_Httpcode_td.append(threading.Thread(target=get_Httpcode))
    for td in get_Httpcode_td:
     td.start()
    time.sleep(60)
    save_td = threading.Thread(target=save_Httpcode)
    save_td.start()
    save_td.join()

if __name__ == '__main__':
    main()
