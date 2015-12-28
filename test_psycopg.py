#!/usr/bin/python
#-*- coding: utf-8 -*-

import uniout
import psycopg2
import pprint

def main():
    conn_string = "host='121.40.34.56' dbname='testPG' user='postgres' password='LYpg&postgres@zzg'"

    print 'connecting to database'
    try:
    # get a connection , if a connection cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string)
    except :
        print 'can not connect to the database'

    cur = conn.cursor()
    cur.execute("drop table NewsList")

    try:
        cur.execute("""CREATE TABLE NewsList (
        tags  TEXT [],
        content TEXT []
        )""")
    except Exception, e:
        pass

    content = "'{ %s, %s ,%s}'" %("我", "爱", "你")
    #first_insert = "'{ a, b, abc}'"
    insert_sql = "INSERT INTO NewsList VALUES ( %s, '{c, d, e}' )" %(content)
    cur.execute(insert_sql)

    "创建 Magazine 数据表语句"

    #"""Create table magazine ("""

    cur.execute("""SELECT * From NewsList""")
    records = cur.fetchall()
    pprint.pprint(records)

if __name__ == "__main__":
    main()