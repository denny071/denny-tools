#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
后台自动化登录
'''
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from time import sleep  # 导入等待 无比重要的等待
import random
import sqlite3


def debugLog(content):
    print("[调试信息]"+content);
    pass

def initChrome():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(
        options=options, executable_path=r'/usr/local/bin/chromedriver')
    browser.maximize_window()    # 最大化页面
    return browser



def initDataPage(browser, url, school, year):
    '''
    初始化页面
    '''
    browser.get(url)
    browser.find_element_by_xpath("/html/body/div[5]/div[1]/div/ul[1]/li[1]/a").click()
    randomWaiting("设置频道")
    setSearch(browser, school, year)
    randomWaiting("设置查询条件")
    getTotalCount(browser, school, year)
    setPageCount(browser)
    randomWaiting("设置显示数量")
    setDataSort(browser)
    randomWaiting("读取数据")
    recomand = recordData(school, year)
    randomWaiting("下一页数据")
    autoRollPage(browser,school, year,recomand)
    

def createCnkiSchoolTable():
    '''
    创建cnki_school表
    '''
    conn = sqlite3.connect('static.db')
    
    debugLog("打开数据库")
    c = conn.cursor()
    sql = "CREATE TABLE cnki_school (id integer PRIMARY KEY autoincrement,"
    sql += "school text not null,"
    sql += "year text not null,"
    sql += "title text not null,"
    sql += "author text not null,"
    sql += "journal text not null,"
    sql += "publich_date text not null,"
    sql += "cited integer not null,"
    sql += "download integer not null);"
    c.execute(sql)
    debugLog("创建表 cnki_school 成功")
    conn.commit()
    conn.close()

def createCnkiSchoolStaticTable():
    '''
    创建cnki_school表
    '''
    conn = sqlite3.connect('static.db')
    
    debugLog("打开数据库")
    c = conn.cursor()
    sql = "CREATE TABLE cnki_school_static (id integer PRIMARY KEY autoincrement,"
    sql += "school text not null,"
    sql += "year text not null,"
    sql += "total integer not null,"
    sql += "recomand integer );"
    c.execute(sql)
    debugLog("创建表 cnki_school_static 成功")
    conn.commit()
    conn.close()

def createCnkiSchoolAuthorTable():
    '''
    创建cnki_school表
    '''
    conn = sqlite3.connect('static.db')
    debugLog("打开数据库")
    c = conn.cursor()
    sql = "CREATE TABLE cnki_school_author (id integer PRIMARY KEY autoincrement,"
    sql += "school text not null,"
    sql += "author text not null,"
    sql += "title text not null);"
    c.execute(sql)
    debugLog("创建表 cnki_school_author 成功")
    conn.commit()
    conn.close()

def insertSql(sql):
    '''
    插入文件
    '''
    conn = sqlite3.connect('static.db')
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()

def getTotalCount(browser, school, year):
    '''
    获得总记录数
    '''
    totalCount = browser.find_element_by_xpath('/html/body/div[5]/div[2]/div[2]/div[2]/form/div/div[1]/div[1]/span[1]/em').text
    totalCount = totalCount.replace(',','')
    debugLog("总共记录" + totalCount)
    sql = "INSERT INTO cnki_school_static (school,year,total) ";
    sql += "VALUES ('" + school + "','" + year + "'," + totalCount + ");"
    debugLog("插入sql语句："+ sql)
    insertSql(sql)
    

def setSearch(browser, school, year):
    '''
    设置查询页面
    '''
    browser.find_element_by_xpath('//*[@id="gradetxt"]/dd[3]/div[2]/div[1]/div[1]/span').click()
    browser.find_element_by_xpath('//*[@id="gradetxt"]/dd[3]/div[2]/div[1]/div[2]/ul[2]/li[5]/a').click()
    browser.find_element_by_xpath('//*[@id="gradetxt"]/dd[3]/div[2]/div[1]/div[2]/ul[2]/li[5]/a').click()
    # 输入查询关键词
    browser.find_element_by_xpath('//*[@id="gradetxt"]/dd[3]/div[2]/input').send_keys(school)
    # 选择查询年份
    browser.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div/input').send_keys(year)
    browser.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div/input').send_keys(year)
    # 单击查询按钮
    browser.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/input').click()

def setPageCount(browser):
    '''
    设置每页记录为50
    '''
    browser.find_element_by_xpath('//*[@id="perPageDiv"]/div/i').click()
    browser.find_element_by_xpath('//*[@id="perPageDiv"]/ul/li[3]').click()
    

def setDataSort(browser):
    '''
    设置排序被引用
    '''
    browser.find_element_by_xpath('//*[@id="orderList"]/li[3]').click()

def autoRollPage(browser,school, year, recomand):
    '''
    自动滚动页面
    '''
    flag=True
    while flag:
        try:
            browser.find_element_by_xpath('//*[@id="PageNext"]').click()
            randomWaiting("下一页")
            recomand = recordData(school, year, recomand)
        except:
            flag=False
            sql = "UPDATE cnki_school_static SET ";
            sql += " recomand = " + str(recomand) + " "
            sql += " WHERE school = '" + school + "' "
            sql += " AND year = '" + year + "';"
            debugLog("更新sql语句："+ sql)
            insertSql(sql)
            debugLog("读取结束")
            close(browser)
            pass
    

def recordData(school, year, recomand = 0):
    '''
    读取网络数据
    '''
    listData = []
    authorSql = "INSERT INTO cnki_school_author (school,author,title) VALUES "
    authorSqlList = []
    for rows in browser.find_element_by_xpath('//*[@id="gridTable"]/table/tbody').find_elements(By.TAG_NAME,"tr"):
        itemData = []
        for item in rows.find_elements(By.TAG_NAME,"td"):
            if item.text != "下载":
                itemData.append(item.text)
        if itemData[-2] != '' and  int(itemData[-2]) > 9:
            recomand = recomand + 1
        for author in itemData[2].split(';'):
            authorSqlList.append("('" + school + "','" + author.strip() + "','[" + year + "]" + itemData[1] + "')")
        listData.append(itemData)
    authorSql = authorSql + ",".join(authorSqlList)
    debugLog("插入authorSql语句："+ authorSql)
    insertSql(authorSql)
    
    makeInsertCnkiSchoolSql(school,year, listData)
    return recomand
 
def makeInsertCnkiSchoolSql(school,year, listData):
    '''
    生成sql
    '''
    sql = "INSERT INTO cnki_school (school,year,title,author,journal,publich_date,cited,download) VALUES "
    valueList = []
    for itemData in listData:
        value = "('"+school+"','" + year+ "','"+ itemData[1]+ "','" + itemData[2]+ "','" + itemData[3]
        value +=  "','" + itemData[4]+ "','" + itemData[5]+ "'," + itemData[6]+ ")" 
        valueList.append(value)
    sql = sql + ",".join(valueList)
    debugLog("插入sql语句："+ sql)
    insertSql(sql)


def randomWaiting(title = ""):
    '''
    随机等待时间
    '''
    waiting = random.randint(10,15);
    debugLog("["+title + "]等待时间："+str(waiting))
    sleep(waiting)

def close(browser):
    '''
    关闭浏览器
    '''
    browser.quit()

def createTable():
    createCnkiSchoolTable()
    createCnkiSchoolStaticTable()
    createCnkiSchoolAuthorTable()

browser = initChrome()
os.remove("static.db")
createTable()
initDataPage(browser,"https://kns.cnki.net/KNS8/AdvSearch?dbcode=SCDB","大连工业大学","2019")



 
 
