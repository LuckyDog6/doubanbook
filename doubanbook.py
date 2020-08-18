import random

import requests
from bs4 import BeautifulSoup
from fontTools.misc import etree
import re
import pymysql


def getHtml(url):
    try:
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
        r=requests.get(url,headers=headers)
        return r.text
    except:
        return ''

def getUrlList(list,list1,html):
    soup=BeautifulSoup(html,'html.parser')
    uls=soup.find('ul',class_='hot-tags-col5 s')

    # lis=uls.find_all('li')
    urls=uls.find_all('a')
    category=uls.find_all('a')

    for i in range(len(urls)):
        list.append('https://book.douban.com'+str(urls[i]['href']))
        list1.append(str(urls[i].text))
    print(list1)
    return list,list1

def getInfo(list,list1,list2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
    for i in range(len(list)):
        r=requests.get(list[i],headers=headers)
        html=r.text
        soup=BeautifulSoup(html,'html.parser')
        lis=soup.find_all('div',class_='info')
        category=list1[i]
        # print(category)
        for i in range(len(lis)):

            try:
                r = requests.get(lis[i].find('a')['href'], headers=headers)
                soup = BeautifulSoup(r.text, 'html.parser')
                info = soup.find('div', id='info')
                wrapper = soup.find('div', id='wrapper')
                mainpic=soup.find('div', id='mainpic')
                img=mainpic.find('img')['src']
                print(img)
                bookname1 = wrapper.find('h1').text
                bookauthor1 = info.find('a').text
                pattern = re.compile(r'\s|\n|<br>', re.S)  # 去除空格
                bookauthor = pattern.sub('', bookauthor1)
                bookname = pattern.sub('', bookname1)
                info1 = info.text
                stock = random.randint(0, 20)
                aaa = re.compile(r'(出版社:)(.*)')
                press1 = aaa.findall(info1)[0][1]
                press = pattern.sub('', press1)
                bbb = re.compile(r'(ISBN:)(.*)')
                isbn1 = bbb.findall(info1)[0][1]
                isbn = pattern.sub('', isbn1)
                ccc = re.compile(r'(定价:)(.*)(元)')
                price1 = ccc.findall(info1)[0][1]
                price = pattern.sub('', price1)
                # 打开数据库连接
                db = pymysql.connect("localhost", "root", "password","ssm-test")
                # 使用cursor()方法获取操作游标
                cursor = db.cursor()
                # SQL 插入语句
                sql = "INSERT INTO book1 (bookId,bookName,bookAuthor,category,price,stock,press,link,img) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val=(isbn,bookname,bookauthor,category,price,stock,press,"'"+lis[i].find('a')['href']+"'",img)
                try:
                    # 执行sql语句
                    cursor.execute(sql,val)
                    # 执行sql语句
                    db.commit()
                    print("insert ok")
                except:
                    # 发生错误时回滚
                    db.rollback()
                    # 关闭数据库连接
                    db.close()
                print(category)
                print(lis[i].find('a')['href'])
                print(bookauthor)
                print(bookname)
                print(isbn)
                print(price)
                print(stock)
                print(press)
            except:
                continue

    #         list2.append(lis[i].find('a')['href'])
    # return list2,category

# def getText(list2,category):
#         # print(len(list2))
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
#         import pymysql
#         for i in list2:
#             r=requests.get(i,headers=headers)
#             soup=BeautifulSoup(r.text,'html.parser')
#             info = soup.find('div', id='info')
#             wrapper=soup.find('div',id='wrapper')
#             bookname=wrapper.find('h1').text
#             bookauthor = info.find('a').text
#             info1=info.text
#
#             aaa = re.compile(r'(出版社:)(.*)')
#             press = aaa.findall(info1)
#
#             bbb = re.compile(r'(ISBN:)(.*)')
#             isbn = bbb.findall(info1)
#
#             ccc = re.compile(r'(定价:)(.*)')
#             price = ccc.findall(info1)
#             print(category)
#             # print(i)
#             # print(bookname)
#             # print(info1)
#             # print(press)
#
#             # print(info)
#             # print(author)
#             # 打开数据库连接
#             # db = pymysql.connect("localhost", "root", "password", "ssm-test")
#             # # 使用cursor()方法获取操作游标
#             # cursor = db.cursor()
#             # # SQL 插入语句
#             # sql = "INSERT INTO url(url) VALUES (%s)"
#             #
#             # try:
#             #     # 执行sql语句
#             #     cursor.execute(sql,author)
#             #     # 执行sql语句
#             #     db.commit()
#             #     print("insert ok")
#             # except:
#             #     # 发生错误时回滚
#             #     db.rollback()
#             # # 关闭数据库连接
#             # db.close()
#             # return ''
#
#
#
#


def main():
    url = 'https://book.douban.com/'
    ulist = []
    ulist1=[]
    ulist2=[]
    str=''
    html = getHtml(url)
    getUrlList(ulist,ulist1,html)
    getInfo(ulist,ulist1,ulist2)
    # getText(ulist2,str)


main()



