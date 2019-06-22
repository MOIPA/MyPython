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
from sentiment_analysis import sentimentAnalysis

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
DataBaseUser = 'root',
DataBasePasswd = '0800',
charset = 'utf8',
use_unicode = False

header_posts = {
    'Host': host,
    'Referer': 'https://m.weibo.cn/u/2557129567?uid=2557129567&luicode=10000011&lfid=100103type%3D1%26q%3D%E5%8D%8E%E4%B8%BA',
    'User-Agent': user_agent
}
header_comments = {
    'Host': host,
    'Referer': 'https://m.weibo.cn/u/2557129567?uid=2557129567&luicode=10000011&lfid=100103type%3D1%26q%3D%E5%8D%8E%E4%B8%BA',
    'User-Agent': user_agent,
    'cookie' : 'ALF=1562915983; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W51j6ZW4SdQaaqgiBzEr0vd5JpX5K-hUgL.Fo-feh.ce0npSKM2dJLoI7_SdcL7qCf09gLA9Btt; _T_WM=22405489250; SCF=Amf5eYkgZqkmzHuRaLDyI3LtU1BRJlQxgJXAqKJq6CJTXKcb-AzaPDytASmp-uYVwXrEnLUyC5UsTXeYrdWYt14.; SUB=_2A25wBNjKDeRhGeNL61sX8ybNzjuIHXVTBviCrDV6PUJbktAKLXjAkW1NSOYLTTJFW2aD7wWB5jJijzhexB9t2S_o; SUHB=0D-1moyhKF9s_v; WEIBOCN_FROM=1110006030; MLOGIN=1; XSRF-TOKEN=2185fd; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1005052557129567'
}
# 连接太多 需要关闭
s = requests.session()
s.keep_alive = False

# 输出数据到文件 改变了print函数的输出位置

# output=sys.stdout
# outputfile=open("D:\\OUTPUT.txt","a",encoding='utf-8')
# sys.stdout=outputfile
# type = sys.getfilesystemencoding()
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

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

# 按页数搜索抓取数据
def get_posts(page,topic):
    url = base_url_posts + 'containerid=100103type'+urllib.parse.quote(search_opt+topic)+'&page='+str(page)
    print('fetching post from url:'+url)
    try:
        response = requests.get(url, headers=header_posts)
        if response.status_code == 200:
            # print(response.json())
            return response.json()
    except requests.ConnectionError as e:
        print('抓取错误', e.args)

# 解析页面返回的json数据
def parse_single_post(json):
    if json==None:
        print('json none')
        exit()
    items = json.get('data').get('cards')
    for item in items:
        item = item.get('card_group')[0].get('mblog')
        if item:
            data = {
                'id': item.get('id'),
                'text': pq(item.get("text")).text(),  # 仅提取内容中的文本
                'attitudes_count': item.get('attitudes_count'),
                'comments_count': item.get('comments_count'),
                'reposts_count': item.get('reposts_count'),
                'created_at':item.get('created_at')
            }
            print(data)
            yield data

# 定义一个类，将连接MySQL的操作写入其中
class mysql_operation:
    def __init__(self):
        self.connect = pymysql.connect(
            host = MySqlHost,
            db = DataBaseName,
            port = DataBasePort,
            user = DataBaseUser,
            passwd = DataBasePasswd,
            charset = 'utf8',
            use_unicode = False
        )
        self.cursor = self.connect.cursor()
    # 通过id查询auto_id(自增id)
    def find_post_id(self,id):
        sql = "select auto_id from post where id = %s"
        try:
            self.cursor.execute(sql,id)
            return self.cursor.fetchall()
        except:
            print('auto_id查找失败')
    # 保存数据到MySQL中 且格式化时间+分析情感
    def save_posts(self,type,theme,id,text,attitudes_count,comments_count,reposts_count,created_at):
        sql = "insert into post(type,theme,id,text,attitudes_count,comments_count,reposts_count,created_at,sentiment) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            self.cursor.execute(sql,(type,theme,id,text,attitudes_count,comments_count,reposts_count,formatTime(created_at),sentimentAnalysis(text)))
            self.connect.commit()
            print('post insert succeed')
            return self.find_post_id(id)
        except Exception as e:
            print('post insert failed',e.args)
    def save_comments(self,post_auto_id,created_at,text,like_count,id,screen_name,profile_url,description,gender,followers_count):
        sql = 'insert into comment(post_id,created_at,text,like_count,user_id,screen_name,profile_url,description,gender,followers_count,sentiment) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            self.cursor.execute(sql,(post_auto_id,formatTime(created_at),text,like_count,id,screen_name,profile_url,description,gender,followers_count,sentimentAnalysis(text)))
            self.connect.commit()
            print('comment insert succeed')
        except Exception as e:
            print('comment insert failed',e.args)
        
 
# 新建对象，然后将数据传入类中
def save_posts(type,theme,id,text,attitudes,comments,reposts,createTime):
    down = mysql_operation()
    return down.save_posts(type,theme,id,text,attitudes,comments,reposts,createTime)

# 数据写入
def writeData(data,path):
    f = open(path,'w',encoding='utf-8')
    f.write(data)
    f.close()
 
# 按页数抓取评论  
def get_comments_by_page(mid,page):
    params = {
        'id' : mid,
        'page': page
    }
    url = base_url_comments + urlencode(params)
    print(url)
    try:
        response = requests.get(url, headers=header_comments)
        if response.status_code == 200:
            # writeData(json.dumps(response.json(),default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False),path)
            return response.json()
    except requests.ConnectionError as e:
        print('fetch error', e.args)

# 解析页面返回的json评论数据
def parse_single_comment(json):
    items = json.get('data').get('data')
    for item in items:
        data = {
            'created_at': item.get('created_at'),
            'text': pq(item.get("text")).text(),  # 仅提取内容中的文本
            'like_count': item.get('like_counts'),
            'user_id':item.get('user').get('id'),
            'user_name':item.get('user').get('screen_name'),
            'user_profile':item.get('user').get('profile_url'),
            'user_description':item.get('user').get('description'),
            'user_gender':item.get('user').get('gender'),
            'user_followers_count':item.get('user').get('followers_count'),
        }
        yield data

def save_comment(post_auto_id,created_at,text,like_count,id,screen_name,profile_url,description,gender,followers_count):
    down = mysql_operation()
    return down.save_comments(post_auto_id,created_at,text,like_count,id,screen_name,profile_url,description,gender,followers_count)

def formatTime(text):
    if re.match(r'.*昨天',text):
        return (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%m-%d")
    if re.match(r'.*小时',text):
        return datetime.datetime.now().strftime("%m-%d")
    return text


# 处理每个帖子的评论 mid:博文id
def processComments(mid,post_auto_id):
    # get the first page json to get the number info
    first_page_json = get_comments_by_page(mid,1)
    try:
        max_page = first_page_json.get('data').get('max')
    except Exception as e:
        print('eror no comment fetched of '+mid)
        return

    if max_page>100:
        max_page=100
    for i in range(1,max_page):
        time.sleep(1)
        try:
            json_data = get_comments_by_page(mid,i)
            results = parse_single_comment(json_data)
            # insert into db
            for result in results:
                save_comment(post_auto_id,result['created_at'],result['text'],result['like_count'],result['user_id'],result['user_name'],result['user_profile'],result['user_description'],result['user_gender'],result['user_followers_count'])
        except Exception as e:
            print('get comments error',e.args)


if __name__ == '__main__':
    #TODO create table by mid

    # arguments control
    if len(sys.argv)!=5:
        print('args error')
        exit()
    type = sys.argv[1]
    theme = sys.argv[2]
    date = sys.argv[3]
    module_id = sys.argv[4]
    # start fetching
    for page in range(1, 1000):   
        jsonData = get_posts(page,theme+'+'+type)
        results = parse_single_post(jsonData)
        for result in results:
            print('fetch page:'+str(page))
            # get all posts and parse the single one
            post_auto_id_array = save_posts(type,theme,result['id'],result['text'],result['attitudes_count'],result['comments_count'],result['reposts_count'],result['created_at'])
            # prepare the material
            post_auto_id = post_auto_id_array[0]
            mid = result['id']
            processComments(mid,post_auto_id)
            

