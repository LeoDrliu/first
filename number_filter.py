# -*-coding=UTF-8-*-
import re
import pymysql


class spilter(object):
    def __init__(self, sentence):
        self.list = sentence
    def cut(self):
        p1 = re.compile(r'[\.\。\？\！\n]')
        list1 = []
        sentence = p1.split(self.list)
        for s in sentence:
            list1.append(s)
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
        print(number)
        return number

if __name__ == '__main__':
    source = input()
    a = spilter(source)
    result = a.cut()
