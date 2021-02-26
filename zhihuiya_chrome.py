#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
后台自动化登录
'''
import os
import random
import sqlite3
import urllib.parse
import json
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from time import sleep 
from browsermobproxy import Server


def debugLog(content):
    print("[调试信息]"+content);
    pass

def isElementExist(browser,element):
    '''
    判断元素是否存在
    '''
    flag=True
    try:
        debugLog(element+"存在")
        browser.find_element_by_xpath(element)
        return flag
    except:
        flag=False
        return flag

def browserProxy():
    server = Server('./browsermob-proxy')
    server.start()
    proxy = server.create_proxy()
    return proxy


def initChrome(url,proxy):
    '''
    初始化浏览器
    '''
    # 启动代理
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--proxy-server={0}'.format(proxy.proxy))
    
    browser = webdriver.Chrome(
        options=options, executable_path=r'/usr/local/bin/chromedriver')
    browser.maximize_window()    # 最大化页面

    # 监听结果
    browser.get(url)
    randomWaiting("打开浏览器")
    return browser

def login(browser, username, password):
    '''
    登录页面
    '''
    browser.find_element_by_xpath('//*[@id="acount"]').send_keys(username)
    browser.find_element_by_xpath('//*[@id="login-ul"]/div/input').send_keys(password)
    browser.find_element_by_xpath('//*[@id="log-button"]').click()
    randomWaiting("开始登录")
    confrimBtn = '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/button[2]'
    if isElementExist(browser,confrimBtn):
        browser.find_element_by_xpath(confrimBtn).click()
    randomWaiting("登录页面")
 
def searchPage(browser,company, query,proxy,pageNumber = 1):
    '''
    查询页面
    '''
    pageSize = 100
    proxy = goPage(pageNumber,pageSize)
    if pageNumber == 1 :
        debugLog("准备读取第1页数据")
    # 读取结果
    for entry in (proxy.har)['log']['entries']:
        if "https://analytics.zhihuiya.com/core-basic-api/analytics/srp/patents" == entry['request']['url'] :
            contentData,groupCount = readJsonData(entry,pageNumber)

    analyzingData(company, contentData)
    pageCount = math.ceil(groupCount/pageSize);
    if pageNumber == 1 and pageCount > 1 :
        for number in range(pageCount - 1):
            debugLog("准备读取第"+ str(number + 2) + "页数据")
            searchPage(browser,company, query,proxy,number + 2)


def goPage(pageNumber,pageSize):
    '''
    跳转页面
    '''
    url = "https://analytics.zhihuiya.com/search/result"
    param = "query#/tablelist/"+ str(pageNumber) +"?sort=sdesc&size=" + str(pageSize)
    searchUrl = url + "?q="+urllib.parse.quote(query)+"&_type=" + param
    debugLog("查询地址：" + searchUrl)
    # 设置代理
    proxy.new_har(options={'captureContent': True,})
    browser.get(searchUrl)
    randomWaiting("查询页面")
    return proxy

def changeStateList(statusList):
    '''
    状态列表
    '''
    statusDesc = {11:"撤回",13:"驳回",222:"PCT国际公布"}
    statesArr = []
    for stateCode in statusList:
        if stateCode in statusDesc:
            statesArr.append(statusDesc[stateCode])
        else:
            statesArr.append(stateCode)
    return ",".join('%s' %value for value in statesArr)
    
def formatApplicant(inventor):
    '''
    格式化申请人
    '''
    data = ",".join(inventor)
    data = data.replace("<span class='patsnap-search-hit'>","")
    data = data.replace("</span>","")
    return data

def analyzingData(company, dataList):
    '''
    读取网络数据
    '''
    debugLog("开始解析数据")
    recordList = []
    inventorList = []
    for data in dataList:
        record = []
        # 公司 
        record.append(company)
        # 公开号 
        record.append(data['PN'])
        # 标题 
        record.append(data['TITLE'])
        # 状态 
        record.append(changeStateList(data['LEGAL_STATUS']))
        # 申请人   
        record.append(formatApplicant(data['ANC']['OFFICIAL']))
        # 发明人 
        record.append(",".join(data['IN']))
        for value in data['IN']:
            inventor = []
            inventor.append(company)
            inventor.append(value)
            inventor.append(data['TITLE'])
            inventorList.append(inventor)
        # 申请日 
        record.append(data['APD'])
        # 公开日 
        record.append(data['PBD'])
        # 添加记录
        recordList.append(record)

    insertDatabase(recordList,inventorList)
 

def insertDatabase(recordList,inventorList):
    '''
    插入数据库
    '''
    sql = "INSERT INTO zhy_data (company, pn,title,status,applicant,inventor,filing_date,public_date) VALUES "
    valueList = []
    for record in recordList:
        value = "('"+ record[0]+"','" + record[1]+ "','" + record[2]+ "','" + record[3]
        value += "','" + record[4] + "','" + record[5]+ "','" + record[6]+ "','" + record[7]+ "')" 
        valueList.append(value)
    sql = sql + ",".join(valueList)
    debugLog("插入sql语句："+ sql)
    insertSql(sql)

    sql = "INSERT INTO zhy_data_inventor (company, inventor,title ) VALUES "
    valueList = []
    for inventor in inventorList:
        value = "('"+ inventor[0]+"','" + inventor[1]+ "','" + inventor[2] + "')" 
        valueList.append(value)
    sql = sql + ",".join(valueList)
    debugLog("插入sql语句："+ sql)
    insertSql(sql)
 
 

def randomWaiting(title = "",waitTime = 5):
    '''
    随机等待时间
    '''
    waiting = random.randint(waitTime,waitTime + 5);
    debugLog("["+title + "]等待时间："+str(waiting))
    sleep(waiting)

def close(browser):
    '''
    关闭浏览器
    '''
    browser.quit()



  
def readJsonData(entry,pageNumber):
    '''
    读取JSOn信息
    '''
    data = json.loads(entry['response']['content']['text'])
    contentData = data['data']['patent_data']
    groupCount = data['data']['patent_count']['group_count']
    debugLog("读取数据")
    if pageNumber == 1:
        totalCount = data['data']['patent_count']['total_count']
        debugLog("总共记录组" + str(groupCount))
        debugLog("总共记录数" + str(totalCount))
        sql = "INSERT INTO zhy_data_static (company,query_str,group_count,total_count) ";
        sql += "VALUES ('" + company + "','" + query + "'," + str(groupCount) + "," + str(totalCount) + ");"
        debugLog("插入sql语句："+ sql)
        insertSql(sql)
    return contentData,groupCount
 

def createZhyDataTable():
    '''
    创建cnki_school表
    '''
    conn = sqlite3.connect('static.db')
    
    debugLog("打开数据库")
    c = conn.cursor()
    sql = "CREATE TABLE zhy_data (id integer PRIMARY KEY autoincrement,"
    sql += "company text not null,"
    sql += "pn text not null,"
    sql += "title text not null,"
    sql += "status text not null,"
    sql += "applicant text not null,"
    sql += "inventor text not null,"
    sql += "filing_date text not null,"
    sql += "public_date text not null);"
    c.execute(sql)
    debugLog("创建表 zhy_data 成功")
    conn.commit()
    conn.close()

def createZhyDataStaticTable():
    '''
    创建cnki_school表
    '''
    conn = sqlite3.connect('static.db')
    
    debugLog("打开数据库")
    c = conn.cursor()
    sql = "CREATE TABLE zhy_data_static (id integer PRIMARY KEY autoincrement,"
    sql += "company text not null,"
    sql += "query_str text not null,"
    sql += "group_count integer,"
    sql += "total_count integer );"
    c.execute(sql)
    debugLog("创建表 zhy_data_static 成功")
    conn.commit()
    conn.close()

def createZhyDataInventorTable():
    '''
    创建cnki_school表
    '''
    conn = sqlite3.connect('static.db')
    debugLog("打开数据库")
    c = conn.cursor()
    sql = "CREATE TABLE zhy_data_inventor (id integer PRIMARY KEY autoincrement,"
    sql += "company text not null,"
    sql += "inventor text not null,"
    sql += "title text not null);"
    c.execute(sql)
    debugLog("创建表 zhy_data_inventor 成功")
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

 

def createDatabase():
    createZhyDataTable()
    createZhyDataStaticTable()
    createZhyDataInventorTable()

proxy = browserProxy()

url = "https://analytics.zhihuiya.com/"

# 删除数据库，仅用于开发
os.remove("static.db")
# 创建数据库
createDatabase()  
# 初始化
browser = initChrome(url,proxy)


# 登录系统
login(browser,"******","******")
company = "江西远东药业有限公司"
# 查询页面
query = "APD:[20160101 TO 20201231] AND ALL_AN:("+ company +")"
dataList = searchPage(browser,company, query, proxy)
 
 




 
 
