# -*- coding: UTF-8 -*-
import pymysql
from snownlp import SnowNLP
import io
import sys
import datetime
# 改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


class MysqlOperation:
    def __init__(self):
        self.connect = pymysql.connect(
            host='39.108.159.175',
            db='weibo_huawei',
            port=3306,
            user='root',
            passwd='0800',
            charset='utf8',
            use_unicode=False
        )
        self.cursor = self.connect.cursor()

    def queryData(self, sql, dataLength):
        try:
            self.cursor.execute(sql)
            # return self.cursor.fetchall()
            count = 0
            while True:
                count += 1
                row = self.cursor.fetchone()
                if not row or count > dataLength:
                    break
                yield row

        except Exception as e:
            print('query data error'+e.args)

    def insertIdAndSentiment(self, comment_id, sentiment):
        sql = 'update comment set sentiment=%s where comment_id=%s'
        try:
            self.cursor.execute(sql, (sentiment, comment_id))
            self.connect.commit()
            print('update sentiment succeed')
        except Exception as e:
            print('update sentiment failed'+e.args)

    def processDataOld(self):
        try:
            sql = 'select comment_id,text from comment'
            self.cursor.execute(sql)
            count = 0
            while True:
                count += 1
                print(str(count))
                (comment_id, text) = self.cursor.fetchone()
                print('fetch one')
                if not text or text == '':
                    continue
                emotionValue = sentimentAnalysis(text.decode('utf-8'))
                print(emotionValue)
                self.insertIdAndSentiment(comment_id, emotionValue)
                # yield(id.decode('utf-8'),emotionValue)
        except Exception as e:
            print(e.args)

    def processData(self):
        try:
            count = 0
            while True:
                count += 1
                print(str(count))
                sql = 'select comment_id,text from comment where sentiment is null limit 10'
                self.cursor.execute(sql)
                results = self.cursor.fetchall()
                if results == ():
                    break
                for result in results:
                    text = result[1]
                    comment_id = result[0]
                    if not text or text == '':
                        continue
                    emotionValue = sentimentAnalysis(text.decode('utf-8'))
                    self.insertIdAndSentiment(comment_id, emotionValue)
        except Exception as e:
            print(e.args)


def fetchText():
    operation = MysqlOperation()
    sql = 'select comment_id,text from comment'
    return operation.queryData(sql, 100)


def processTextAndAnalysis():
    operation = MysqlOperation()
    return operation.processData()


def sentimentAnalysis(text):
    #pre = datetime.datetime.now()
    if text == '' or not text:
        return 0
    textArray = SnowNLP(text)
    result = 0
    for s in textArray.sentences:
        result += SnowNLP(s).sentiments
        # print(s+' sentiment value：'+str(SnowNLP(s).sentiments))
    #now = datetime.datetime.now()
    # print(now-pre)
    return result/len(textArray.sentences) if len(textArray.sentences) != 0 else 0


if __name__ == '__main__':
    print(sentimentAnalysis(''))
    # data = fetchText()
    # for text in data:
    # print(text[1].decode('utf-8')+str(sentimentAnalysis(text[1].decode('utf-8'))))
    values = processTextAndAnalysis()
    # for value in values:
    # print(value)
