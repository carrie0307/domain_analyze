# 基础数据统计
---
**只统计top10**
## TLD

**benign**
```
SELECT tld, COUNT(*) num FROM whois WHERE ID IN (SELECT ID FROM other_info WHERE web_judge_result = 1) GROUP BY tld  ORDER BY num DESC ;
```

| TLD        | COUNT           |
| ------------- |:-------------:|
| com | 5014 |
| cn | 1090      |
| net      | 706 |
| cc | 210     |
| org      | 176 |
| info | 34      |
| tv      | 25 |
| me |18     |
| biz      | 18 |
| co | 4     |


**malicious**
```
SELECT tld, COUNT(*) num FROM whois WHERE ID IN (SELECT ID FROM other_info WHERE web_judge_result = 2 OR web_judge_result = 3) GROUP BY tld  ORDER BY num DESC LIMIT 10;
```

| TLD        | COUNT           |
| ------------- |:-------------:|
| com | 12290 |
| cc | 8529      |
| pw      |1012|
| cn | 980    |
| net      | 442|
| win | 170      |
| top      | 170  |
| tk |167     |
|info      | 91|
| xyz | 70    |

## email

**benign**
```
SELECT RIGHT(reg_email, LENGTH(reg_email)-instr(reg_email,'@')) email_type, COUNT(*) num FROM whois WHERE ID IN (SELECT ID FROM other_info WHERE web_judge_result = 1) GROUP BY email_type ORDER BY num DESC;
```
| Emial_type       | COUNT         |
| ------------- |:-------------:|
| -- | 2098 |
| qq.com |1501    |
| 163.com      |637 |
| 126.com | 384   |
| YinSiBaoHu.AliYun.com | 349 |
| gmail.com |313    |
| hotmail.com     | 87 |
| sina.com |71    |
| outlook.com      |53|
|foxmail.com | 43   |

**malicious**
```
SELECT RIGHT(reg_email, LENGTH(reg_email)-instr(reg_email,'@')) email_type, COUNT(*) num FROM whois WHERE ID IN (SELECT ID FROM other_info WHERE web_judge_result = 2 OR web_judge_result = 3) GROUP BY email_type ORDER BY num DESC;
```

| Emial_type       | COUNT         |
| ------------- |:-------------:|
| -- | 11142 |
| qq.com | 4874     |
| YinSiBaoHu.AliYun.com      | 3150 |
| 163.com | 2184     |
| gmail.com      | 704 |
| 126.mail |649     |
| sina.com     | 172 |
| privacyprotect.org |137    |
| hotmail.com      | 83|
|juming.com | 81     |

## 注册商

**benign**

```
SELECT sponsoring_registrar, COUNT(*) num FROM whois WHERE ID IN (SELECT ID FROM other_info WHERE web_judge_result = 1) GROUP BY sponsoring_registrar ORDER BY num DESC;
```

| Sponsoring_registrar       | COUNT         |
| ------------- |:-------------:|
| -- | 1471|
| HICHINA ZHICHENG TECHNOLOGY LTD. |1232   |
| XINNET TECHNOLOGY CORPORATION      |644 |
| eName Technology Co., Ltd. | 416  |
| West263 International Limited| 291 |
|阿里云计算有限公司（万网） |226    |
|Bizcn.com,Inc.  | 222 |
| 22NET, INC. |183  |
|SHANGHAI MEICHENG TECHNOLOGY INFORMATION DEVELOPMENT CO., LTD. |146|
|Beijing Innovative Linkage Technology Ltd. dba dns.com.cn| 146 |

**malicious**

```
SELECT sponsoring_registrar, COUNT(*) num FROM whois WHERE ID IN (SELECT ID FROM other_info WHERE web_judge_result = 2 OR web_judge_result = 3) GROUP BY sponsoring_registrar ORDER BY num DESC;
```

| Sponsoring_registrar       | COUNT         |
| ------------- |:-------------:|
| -- | 10687|
| HICHINA ZHICHENG TECHNOLOGY LTD. |3522|
| XINNET TECHNOLOGY CORPORATION      |2382|
| SHANGHAI MEICHENG TECHNOLOGY INFORMATION DEVELOPMENT CO., LTD.|1809|
| Bizcn.com,Inc.| 753|
|PDR Ltd. d/b/a PublicDomainRegistry.com|711 |
|West263 International Limited | 685|
| ENOM, INC.|423|
|22NET, INC.|396|
|eName Technology Co., Ltd.| 337|

##敏感词

**benign**
```
SELECT RIGHT(flag,1) symbol, COUNT(*) num FROM malicious_info WHERE ID IN (SELECT ID FROM other_info WHERE web_judge_result = 2 OR web_judge_result = 3) GROUP BY symbol ORDER BY num DESC;
```
| flag        | COUNT           |
| ------------- |:-------------:|
| 8| 3508 |
| 9 | 3335     |
| 2     |307|
| 1 | 165|
| 0 | 1    |


**malicious**
```
SELECT RIGHT(flag,1) symbol, COUNT(*) num FROM malicious_info WHERE ID IN (SELECT ID FROM other_info WHERE web_judge_result = 2 OR web_judge_result = 3) GROUP BY symbol ORDER BY num DESC;
```
| flag        | COUNT           |
| ------------- |:-------------:|
| 8| 19442 |
| 9 | 2683      |
| 2     |2106|
| 1 | 116    |


## 地理位置比对

**benign**
```
SELECT cmp, COUNT(*) num FROM locate WHERE ID IN (SELECT ID FROM other_info WHERE web_judge_result = 1) GROUP BY cmp ORDER BY num DESC;
```
| cmp        | COUNT           |
| ------------- |:-------------:|
| -2| 4697 |
| 22 | 1156 |
| 33    |488|
| 11 |349 |
| 21| 312|
| 32   |182 |
| 0 |113|
| 31| 14|
| 10| 4 |
| 23 | 2 |
| 44|1|

**malicious**
```
SELECT cmp, COUNT(*) num FROM locate WHERE ID IN (SELECT ID FROM other_info WHERE web_judge_result = 1) GROUP BY cmp ORDER BY num DESC;
```
| cmp        | COUNT           |
| ------------- |:-------------:|
| -2| 13700 |
| 11 | 4333 |
| 22    |2397|
| 0 |1903 |
| 21| 1067|
| 33 |548|
| 32 |170|
| 10| 101|
| 31| 9 |
| 12 | 1 |
| 1|1|

---
*几个要注意的地方：
1.cmp为0的实际是没有运行结果的;
2.以上划分的粒度待定，先这样确定作为测试
3.ttl的问题
---
暂时整理这些特征项
2017.08.24
