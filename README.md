# -*-coding=UTF-8-*-
import docx
import re
import pymysql


class spilter(object):
    def __init__(self, user1, user2, db1, db2, pass1, pass2):
        self.user1 = user1
        self.user2 = user2
        self.db1 = db1
        self.db2 = db2
        self.password1 = pass1
        self.password2 = pass2

    def cut(self):
        db1 = pymysql.connect(host='localhost', port=3306, user=self.user1, passwd=self.password1, db=self.db1, charset='utf8')
        cursor_search = db1.cursor()
        sql_search = """(SELECT * FROM TABLE1)"""
        cursor_search.execute(sql_search)
        file = cursor_search.fetchall()
        p1 = re.compile(r'[\.\。\？\！]')
        list1 = []
        for row in file:
            sentence = p1.split(row[1])
            for s in sentence:
                list1.append(s)
        db = pymysql.connect(host='localhost', port=3306, user=self.user2, passwd=self.password2, db=self.db2, charset='utf8')
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
        sql_create = """CREATE TABLE EMPLOYEE(
            sentence_id int ,
            phone_number char(15) not null,
            sent text not null,
            primary key(sentence_id)
            )"""
        cursor.execute(sql_create)
        phone1 = re.compile(r'(?<!\d)1[3|4|5|7|8]\d{9}(?!\d)')
        phone2 = re.compile(
            r'(?<!\d)1[3|4|5|7|8](?:\d\s+\d{4}\s+\d{4}|\d{2}\s+\d{3}\s+\d{4}|\d{2}\s+\d{4}\s+\d{3})(?!\d)')
        phone3 = re.compile(r'(?<!\d)9\d{7}(?!\d)')
        replace = re.compile(' ')
        number = []
        for x in range(len(list1)):
            t = []
            for tmp in phone1.findall(list1[x]):
                a = [x, tmp, list1[x]]
                t.append(a)
            for tmp in phone2.findall(list1[x]):
                tmp = replace.sub('', tmp)
                a = [x, tmp, list1[x]]
                t.append(a)
            for tmp in phone3.findall(list1[x]):
                tmp = '852-' + tmp
                a = [x, tmp, list1[x]]
                t.append(a)
            for y in t:
                number.append(y)
                for z in y:
                    print(z)
        sql_insert = "INSERT INTO EMPLOYEE VALUES(%s,%s,%s)"
        try:
            cursor.executemany(sql_insert, number)
            db.commit()
        except:
            db.rollback()
        cursor.close()
        db.close()

if __name__ == '__main__':
    a = spilter("root","root","test_db","database_name","123","123")
    a.cut()
