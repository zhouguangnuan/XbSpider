# -*- coding: utf-8 -*-
import datetime

import MySQLdb

from XbSpider.settings import KEYWORD, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME

__author__ = 'bobby'
import hashlib
import re

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

# 通过标题计算招标类型
def get_type(title):
    type = 1 # 默认【其它】
    match_re = re.match(".*(" + KEYWORD + ").*", title)
    if match_re:
        type = 2
    return type

def strptime(value, format):
    try:
        create_date = datetime.datetime.strptime(value, format).date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date

def get_match_result(pattern, string, group_num):
    _pattern = re.compile(r"(" + pattern + ")")
    match_re = re.search(_pattern, string)
    if match_re:
        return match_re.group(group_num)
    else:
        return None

def find_last_hospital_procurement_item(cityId, hospitalId):
    # 链接数据库
    db = MySQLdb.connect(
        MYSQL_HOST,
        MYSQL_USER,
        MYSQL_PASSWORD,
        MYSQL_DBNAME,
        charset="utf8",
        use_unicode=True)
    cursor = db.cursor()
    # sql为你的查询语句
    sql = "SELECT originalUrl, createTime FROM massage_hospital_procurement WHERE cityId = %s AND hospitalId = %s ORDER BY createTime DESC LIMIT 0 , 1"
    cursor.execute(sql, (cityId, hospitalId))
    result = cursor.fetchone()
    db.close()  # 关闭数据库
    return result


if __name__ == "__main__":
    print (get_match_result('[\d]{4}-[\d]{2}-[\d]{2}', '［发布时间： 2019-05-14  信息来源：', 1))