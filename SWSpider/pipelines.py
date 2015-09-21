# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import Flight
from datetime import datetime as dt
import sqlite3
import json


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

    def process_item(self, item, spider):
        filename = 'prices'
        f = open(filename, 'a')
        f.write(str(item))
        f.write('\r\n')

