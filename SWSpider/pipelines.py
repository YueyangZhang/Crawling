# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import Flight
from datetime import datetime as dt
import sqlite3


class InsertDBPipeline(object):

    def __init__(self):
        self.conn = sqlite3.connect('swa.db')
        self.c = self.conn.cursor()
        self.create_table()

    def process_item(self, item, spider):
        query = "INSERT INTO flights VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        data = (dt.now(), item["depCity"], item["arrCity"], item["depDate"],
                item["arrDate"], str(item["flights"]),
                int(item["price"]), int(item["stops"]))
        if (isinstance(item, Flight)):
            self.c.execute(query, data)
            self.conn.commit()

    def create_table(self):
        create_table_sql = "CREATE TABLE IF NOT EXISTS 'flights' ('id' int(11) NOT NULL,'depCity' varchar(10) NOT NULL,'arrCity' varchar(10) NOT NULL,'depDate' varchar(10) NOT NULL,'arrDate' varchar(10) NOT NULL,'flights' varchar(10) NOT NULL,'price' int(11) NOT NULL,'stop' int(11) NOT NULL,PRIMARY KEY ('id'))"
        self.c.execute(create_table_sql)
        self.conn.commit()


class OutputJsonPipeline(object):
    minimum_price = 0

    def process_item(self, item, spider):
        self.item = item
        if self.minimum_price == 0 : 
            self.minimum_price = int(item['price'])
        else :
            self.minimum_price = min(self.minimum_price,int(item['price']))

    def close_spider(self, spider):
        print('Writing depCity:'+self.item['depCity']+' arrCity:'+self.item['arrCity']+' =='+str(self.minimum_price)+'==')
        f = open(self.item['filename'], 'a')
        f.write('x:'+str(self.item['x'])+' y:'+str(self.item['y'])+' price:'+str(self.minimum_price))
        f.write('\r\n')
