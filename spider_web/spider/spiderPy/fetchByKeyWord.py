# -*- coding: utf-8 -*-
import requests
import sys
import time
import io
import urllib
import urllib.request
import re
import bs4
import pymysql
import json
import datetime

from urllib.parse import urlencode
from pyquery import PyQuery as pq
from spider.spiderPy.sentiment_analysis import sentimentAnalysis

TablePostName = ''
TableCommentName = ''
path = '/home/william/OUTPUT.txt'
search_opt = '=1&q='
host = 'm.weibo.cn'
base_url_posts = 'https://%s/api/container/getIndex?' % host
base_url_comments = 'https://%s/api/comments/show?' % host
user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
# DB
MySqlHost = '39.108.159.175'
DataBaseName = 'weibo_huawei'
DataBasePort = 3306
DataBaseUser = 'root'
DataBasePasswd = '0800'

STOP = False

# Head
header_posts = {
    'Host': host,
    'Referer': 'https://m.weibo.cn/u/2557129567?uid=2557129567&luicode=10000011&lfid=100103type%3D1%26q%3D%E5%8D%8E%E4%B8%BA',
    'User-Agent': user_agent
}
header_comments = {
    'Host': host,
    'Referer': 'https://m.weibo.cn/u/2557129567?uid=2557129567&luicode=10000011&lfid=100103type%3D1%26q%3D%E5%8D%8E%E4%B8%BA',
    'User-Agent': user_agent,
    'cookie': 'ALF=1562915983; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W51j6ZW4SdQaaqgiBzEr0vd5JpX5K-hUgL.Fo-feh.ce0npSKM2dJLoI7_SdcL7qCf09gLA9Btt; _T_WM=22405489250; SCF=Amf5eYkgZqkmzHuRaLDyI3LtU1BRJlQxgJXAqKJq6CJTXKcb-AzaPDytASmp-uYVwXrEnLUyC5UsTXeYrdWYt14.; SUB=_2A25wBNjKDeRhGeNL61sX8ybNzjuIHXVTBviCrDV6PUJbktAKLXjAkW1NSOYLTTJFW2aD7wWB5jJijzhexB9t2S_o; SUHB=0D-1moyhKF9s_v; WEIBOCN_FROM=1110006030; MLOGIN=1; XSRF-TOKEN=2185fd; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1005052557129567'
}
# 连接太多 需要关闭
s = requests.session()
s.keep_alive = False

# 过滤沙雕网名


def textFilter(text):
    # m_name = re.match(r'\s*回复@.*:(.*)', text)
    # if m_name:
    #    text = m_name.group(1)
    return re.sub(r'(回复)?@.*?:', '', text)

# 映射情感值 -1~1


def MappingSentimentValue(text):
    text = textFilter(text)
    value = sentimentAnalysis(text)
    value -= 0.5
    value *= 2
    return value

# 按页数抓取数据


def get_posts_old(page):
    params = {
        'type': 'uid',
        'value': 5561876124,
        'containerid': 1076032557129567,
        'page': page
    }
    url = base_url_posts + urlencode(params)
    try:
        response = requests.get(url, headers=header_posts)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('抓取错误', e.args)
        sys.stdout.flush()

# 按页数搜索抓取数据


def get_posts(page, topic):
    url = base_url_posts + 'containerid=100103type' + \
        urllib.parse.quote(search_opt+topic)+'&page='+str(page)
    print('fetching post from url:'+url)
    sys.stdout.flush()
    try:
        response = requests.get(url, headers=header_posts)
        if response.status_code == 200:
            # print(response.json())
            return response.json()
    except requests.ConnectionError as e:
        print('抓取错误', e.args)
        sys.stdout.flush()

# 解析页面返回的json数据


def parse_single_post(json_data):
    global STOP
    if json_data == None:
        print('json none')
        sys.stdout.flush()
        # exit()
        STOP = True
        return
    items = json_data.get('data').get('cards')
    for item in items:
        try:
            item = item.get('card_group')[0].get('mblog')
        except:
            print('no data searched in weibo')
            sys.stdout.flush()
            # exit()
            STOP = True
            return
        # try:
        if item:
            data = {
                'id': item.get('id'),
                'text': item.get('text'),  # 仅提取内容中的文本
                'attitudes_count': item.get('attitudes_count'),
                'comments_count': item.get('comments_count'),
                'reposts_count': item.get('reposts_count'),
                'created_at': item.get('created_at')
            }
            print(data)
            sys.stdout.flush()
            yield data
        # except:
        #    print(item)
        #    sys.stdout.flush()

# 定义一个类，将连接MySQL的操作写入其中


class mysql_operation:
    def __init__(self):
        self.connect = pymysql.connect(
            host=MySqlHost,
            db=DataBaseName,
            port=DataBasePort,
            user=DataBaseUser,
            passwd=DataBasePasswd,
            charset='utf8',
            use_unicode=False
        )
        self.cursor = self.connect.cursor()
    # create table

    def createTable(self, module_id):
        module_id = int(module_id)
        dropSql = "drop table post_%s,comment_%s"
        createCommentSql = "CREATE TABLE `comment_%s` (   `comment_id` int(11) NOT NULL AUTO_INCREMENT,   `post_id` int(11) NOT NULL,   `text` text NOT NULL,   `created_at` varchar(64) DEFAULT NULL,   `like_count` int(11) DEFAULT NULL,   `user_id` varchar(64) DEFAULT NULL,   `screen_name` varchar(64) DEFAULT NULL,   `profile_url` varchar(64) DEFAULT NULL,   `description` varchar(64) DEFAULT NULL,   `gender` varchar(32) DEFAULT NULL,   `followers_count` int(11) DEFAULT NULL,   `sentiment` float DEFAULT NULL,   PRIMARY KEY (`comment_id`),   KEY `comment_ibfk_1` (`post_id`)) ENGINE=InnoDB AUTO_INCREMENT=9797 DEFAULT CHARSET=utf8;"
        createPostSql = "CREATE TABLE `post_%s` (   `id` varchar(64) NOT NULL,   `text` text NOT NULL,   `attitudes_count` int(11) DEFAULT NULL,   `comments_count` int(11) DEFAULT NULL,   `reposts_count` int(11) DEFAULT NULL,   `created_at` varchar(64) DEFAULT NULL,   `auto_id` int(11) NOT NULL AUTO_INCREMENT,   `theme` varchar(32) DEFAULT NULL,   `type` varchar(32) DEFAULT NULL,   `sentiment` float DEFAULT NULL,   PRIMARY KEY (`auto_id`) ) ENGINE=InnoDB AUTO_INCREMENT=260 DEFAULT CHARSET=utf8"
        try:
            self.cursor.execute(dropSql, (module_id, module_id))
        except:
            print('no table no drop')
            sys.stdout.flush()
        try:
            self.cursor.execute(createCommentSql, module_id)
            self.cursor.execute(createPostSql, module_id)
            self.connect.commit()
            # self.connect.close()
        except Exception as e:
            print('drop failed', e.args)
            sys.stdout.flush()

    # 通过id查询auto_id(自增id)
    def find_post_id(self, id):
        global TablePostName
        sql = "select auto_id from "+TablePostName+" where id = %s"
        try:
            self.cursor.execute(sql, id)
            return self.cursor.fetchall()
        except:
            print('auto_id查找失败')
            sys.stdout.flush()
    # 保存数据到MySQL中 且格式化时间+分析情感

    def save_posts(self, type, theme, id, text, attitudes_count, comments_count, reposts_count, created_at):
        sql = "insert into "+TablePostName + \
            "(type,theme,id,text,attitudes_count,comments_count,reposts_count,created_at,sentiment) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            self.cursor.execute(sql, (type, theme, id, textFilter(text), attitudes_count, comments_count,
                                      reposts_count, formatTime(created_at), MappingSentimentValue(text)))
            self.connect.commit()
            print('post insert succeed')
            sys.stdout.flush()
            return self.find_post_id(id)
        except Exception as e:
            print('post insert failed', e.args)
            sys.stdout.flush()

    def save_comments(self, post_auto_id, created_at, text, like_count, id, screen_name, profile_url, description, gender, followers_count):
        sql = 'insert into '+TableCommentName + \
            '(post_id,created_at,text,like_count,user_id,screen_name,profile_url,description,gender,followers_count,sentiment) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            self.cursor.execute(sql, (post_auto_id, formatTime(created_at),
                                      textFilter(text), like_count, id,
                                      screen_name, profile_url, description, gender, followers_count, MappingSentimentValue(text)))
            self.connect.commit()
            print('comment insert succeed')
            sys.stdout.flush()
        except Exception as e:
            print('comment insert failed', e.args)
            sys.stdout.flush()


# 新建对象，然后将数据传入类中
def save_posts(type, theme, id, text, attitudes, comments, reposts, createTime):
    down = mysql_operation()
    return down.save_posts(type, theme, id, text, attitudes, comments, reposts, createTime)

# create table


def createTable(module_id):
    down = mysql_operation()
    down.createTable(module_id)

# 数据写入


def writeData(data, path):
    f = open(path, 'w', encoding='utf-8')
    f.write(data)
    f.close()

# 按页数抓取评论


def get_comments_by_page(mid, page):
    params = {
        'id': mid,
        'page': page
    }
    url = base_url_comments + urlencode(params)
    print(url)
    sys.stdout.flush()
    try:
        response = requests.get(url, headers=header_comments)
        if response.status_code == 200:
            # writeData(json.dumps(response.json(),default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False),path)
            return response.json()
    except requests.ConnectionError as e:
        print('fetch error', e.args)
        sys.stdout.flush()

# 解析页面返回的json评论数据


def parse_single_comment(json):
    items = json.get('data').get('data')
    for item in items:
        data = {
            'created_at': item.get('created_at'),
            'text': pq(item.get("text")).text(),  # 仅提取内容中的文本
            'like_count': item.get('like_counts'),
            'user_id': item.get('user').get('id'),
            'user_name': item.get('user').get('screen_name'),
            'user_profile': item.get('user').get('profile_url'),
            'user_description': item.get('user').get('description'),
            'user_gender': item.get('user').get('gender'),
            'user_followers_count': item.get('user').get('followers_count'),
        }
        yield data


def save_comment(post_auto_id, created_at, text, like_count, id, screen_name, profile_url, description, gender, followers_count):
    down = mysql_operation()
    return down.save_comments(post_auto_id, created_at, text, like_count, id, screen_name, profile_url, description, gender, followers_count)


def formatTime(text):
    if re.match(r'.*昨天', text):
        return
    (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    if re.match(r'.*小时', text):
        return datetime.datetime.now().strftime("%Y-%m-%d")
    if re.match(r'.*分钟', text):
        return datetime.datetime.now().strftime("%Y-%m-%d")
    if not re.match(r'\d{4}-\d{2}-\d{2}', text):
        return datetime.datetime.now().strftime('%Y-')+text

    return text


# 处理每个帖子的评论 mid:博文id
def processComments(mid, post_auto_id):
    # get the first page json to get the number info
    first_page_json = get_comments_by_page(mid, 1)
    try:
        max_page = first_page_json.get('data').get('max')
    except Exception as e:
        print('eror no comment fetched of '+mid, e.args)
        sys.stdout.flush()
        return

    if max_page > 100:
        max_page = 100
    for i in range(1, max_page):
        time.sleep(1)
        try:
            json_data = get_comments_by_page(mid, i)
            results = parse_single_comment(json_data)
            # insert into db
            for result in results:
                save_comment(post_auto_id, result['created_at'], result['text'], result['like_count'], result['user_id'], result['user_name'],
                             result['user_profile'], result['user_description'], result['user_gender'], result['user_followers_count'])
        except Exception as e:
            print('get comments error', e.args)
            sys.stdout.flush()


def startSpider(t_type, t_theme, t_date, t_module_id, t_drop):
    global STOP
    STOP = False
    TablePostPrefix = 'post_'
    TableCommentPrefix = 'comment_'
    type = t_type
    theme = t_theme
    date = t_date
    module_id = t_module_id

    global TablePostName
    global TableCommentName

    TablePostName = TablePostPrefix+str(module_id)
    TableCommentName = TableCommentPrefix+str(module_id)
    # create table by mid
    if int(t_drop) == 1:
        createTable(module_id)
    # start fetching
    for page in range(1, 3):
        print('fetch page:'+str(page))
        if STOP:
            return
        jsonData = get_posts(page, theme+'+'+type)
        results = parse_single_post(jsonData)
        for result in results:
            sys.stdout.flush()
            # get all posts and parse the single one
            try:
                post_auto_id_array = save_posts(
                    type, theme, result['id'], result['text'], result['attitudes_count'], result['comments_count'], result['reposts_count'], result['created_at'])
            # prepare the material
                post_auto_id = post_auto_id_array[0]
            except Exception as e:
                print('error insert into db ,post_id:'+str(post_auto_id_array), e.args)
                sys.stdout.flush()
                continue
            mid = result['id']
            processComments(mid, post_auto_id)

if __name__ == '__main__':
    # startSpider()
    pass
