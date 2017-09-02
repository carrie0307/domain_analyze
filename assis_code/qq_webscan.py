# coding:utf-8
'''
 获取腾讯电脑管家网站检测结果
'''
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from timeout import timeout
import os
import MySQLdb
import Queue

'''
1.png -- 1
2.png，3.png -- 2 危险
48_money.png -- 2 危险
6.png -- 4 未知
'''

domains_q = Queue.Queue()
webscan_map = {'1.png': '1', '2.png': '2', '3.png': '2', '6.png': '4', '48_money.png': '2'}

conn = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys")
cur=conn.cursor()
def get_domains():
    '''
    获取要处理的域名
    '''
    global domains_q
    SQL = "SELECT ID, domain FROM domain_index WHERE source = '103' and ID not in (SELECT ID from other_info)"
    cur.execute(SQL)
    result = cur.fetchall()
    domains_q = Queue.Queue()
    for item in result:
        domains_q.put([int(item[0]), str(item[1])])
# cur.close()
# conn.close()

def kill_process():
    '''
    杀掉phantomjs的进程
    '''
    print 'kill processes ...\n'
    r = os.popen("ps -ef|grep 'phantomjs' |grep -v grep |awk '{print $2}'")
    text = r.read()
    r.close()
    pids = text.split('\n')
    for pid in pids:
        cmd = "kill " + pid
        print cmd
        os.system(cmd)


@timeout(10) # 防止卡死的情况
def phantomjs_get_html(driver):
    '''
    通过phantomjs获取判断结果的页面
    '''
    driver.get("https://guanjia.qq.com/online_server/webindex.html")
    driver.find_element_by_id("search_site").send_keys(str(domain))
    driver.find_element_by_id("search_button").click()
    driver.implicitly_wait(5) # 隐式等待10s
    page = etree.HTML(driver.page_source)
    return page


def get_judge_res(page):
    '''
    从判断将结果页面中获取判断结果
    '''
    global webscan_map
    url = page.xpath('//*[@id="score_img"]/img/@src')[0]
    img = str(str(url).split('/')[-1]) # 获取图片名称（编号）
    qq_judge = webscan_map[img]
    return qq_judge



def save_res(res_list):
    '''
    存储结果
    '''
    print 'save res ...\n'
    for item in res_list:
        # sqlstr = "INSERT INTO other_info(ID,web_judge_result) VALUES(%s,'%s')" %(item[0], item[1])
        sqlstr = "UPDATE other_info SET web_judge_result = '%s' WHERE ID = %s" %(item[1], item[0])
        cur.execute(sqlstr)
    conn.commit()
    print 'res saved ...\n'


if __name__ == '__main__':
    counter = 0
    get_domains()
    res_list = []
    driver = webdriver.PhantomJS(executable_path="/usr/local/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
    while True:
        if not domains_q.empty():
            ID, domain = domains_q.get()
        else:
            break
        try:
            page = phantomjs_get_html(driver)
            qq_judge = get_judge_res(page)
            res_list.append([ID,qq_judge])
            print 'NO.' + str(counter) + '  ' + domain + '  ' + qq_judge
        except:
            # 可能出现卡死导致的Timeout
            # page.xpath('//*[@id="score_img"]/img/@src')提取不到或判断结果为load.gif
            domains_q.put([ID, domain])
            continue
        counter += 1
        if counter%99 == 0:
            try:
                save_res(res_list)
            except Exception, e:
                print str(e)
                print '存储出错 ...'
            res_list = []
            try:
                driver.close()
                driver.quit()
            except: #  不能正常关闭则杀掉进程
                kill_process()
            finally:
                driver = webdriver.PhantomJS(executable_path="/usr/local/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
    save_res(res_list)
    cur.close()
    conn.close()
