#coding=utf-8
'''
点击腾讯新闻
'''
from selenium import webdriver
import random
import time
import datetime
import pymysql
import logging
import configparser
import os



config = configparser.ConfigParser()
config.read('config.ini')  

# -------------  配置信息 start ----------------------------
# 打开页面最小时间
open_min_time = int(config['config']['open_min_time'])
# 打开页面最大时间
open_max_time = int(config['config']['open_max_time'])
# 看广告最小时间
ad_min_time = int(config['config']['ad_min_time'])
# 看广告最大时间
ad_max_time = int(config['config']['ad_max_time'])
# 程序休眠开始时间 几点
sleep_start_hour = int(config['config']['sleep_start_hour'])
# 程序休眠结束时间 几点
sleep_stop_hour = int(config['config']['sleep_stop_hour'])
# 执行间隔时间
rest_min_time = int(config['config']['rest_min_time'])
# 执行间隔时间
rest_max_time = int(config['config']['rest_max_time'])
# 是否开启浏览器
show_browser = config['config']['show_browser']
# 是否开启浏览器
download_default_directory = config['config']['download_default_directory']

# 数据库信息
mysql_host = config['mysql']['mysql_host']
mysql_user = config['mysql']['mysql_user']
mysql_password = config['mysql']['mysql_password']
mysql_db = config['mysql']['mysql_db']
mysql_table = config['mysql']['mysql_table']

# 当前更新小时
now_update_hour = -1;



# -------------  配置信息 end  ----------------------------

# -------------  初始化信息 start ----------------------------
def openBrowser():
    if show_browser == 'on':
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': download_default_directory}
        options.add_experimental_option('prefs', prefs)
        # 打开游览器
        browser = webdriver.Chrome(options=options)
    else:
        options = webdriver.ChromeOptions()
        # 使用headless无界面浏览器模式
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless') 
        options.add_argument('--disable-gpu')
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': download_default_directory}
        options.add_experimental_option('prefs', prefs)
        # 启动浏览器，获取网页源代码
        browser = webdriver.Chrome(options=options)
    
    return browser




# -------------  初始化信息 end ----------------------------

count = 0


def writeLog(message):
    pathinfo = os.path.dirname(__file__) + "logs/"
    if config['config']['show_log'] == 'on':
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"  
        DATE_FORMAT = "%Y/%m/%d %H:%M:%S %p"                    
        fp = logging.FileHandler(pathinfo + str(datetime.date.today()) + '-click-logs.txt', encoding='utf-8')
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp])  
        logging.info(message)
    else:
        print(message)

# 单击广告
def clickAd(browser, url, open_time, ad_time):
    # 打开浏览器
    browser.get(url)
    # 浏览新闻时间
    time.sleep(open_time)
    browser.find_element_by_css_selector(".down_img").click()
    # 广告时间
    time.sleep(ad_time)

# 通过MySQL数据获取数据
def getUrlList():
    data_list = []
    try:
        # 打开数据库连接
        db = pymysql.connect(mysql_host,mysql_user,mysql_password,mysql_db)
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        cursor.execute( "SELECT `title`,`tecent_url` FROM `"+ mysql_table +"` ORDER BY `id` DESC LIMIT 500 ")
        results = cursor.fetchall()# 获取所有记录列表
        for row in results:
            data_list.append({'title':row[0],'url':row[1]})
        # 关闭数据库连接
    except Exception as e:
        writeLog('数据库连接错误:'+str(e))
    finally:
        db.close()
    return data_list

# 计算休息时间
def calSleepTime(sleep_stop_hour):
    stop_time = datetime.datetime.now().replace(hour=sleep_stop_hour,minute=0,second=0,microsecond=0);
    now_time = datetime.datetime.now().replace(microsecond=0)
    sleep_second = int((stop_time - now_time).total_seconds())
    minute, second = divmod(sleep_second, 60)
    hour, minute = divmod(minute, 60)
    writeLog('还需要等待%d小时%02d分钟%02d秒后程序启动'% (hour, minute, second))
    return sleep_second

# 执行任务
def runTask(data_list, open_min_time,open_max_time,ad_min_time,ad_max_time):
    browser = openBrowser()
    data = random.choice(data_list)
    writeLog('访问:' + data['title'])
    open_time = random.randint(open_min_time,open_max_time)
    writeLog('内容停留时间:'+str(open_time))
    ad_time = random.randint(ad_min_time, ad_max_time)
    writeLog('广告停留时间:' + str(ad_time))
    clickAd(browser, data['url'], open_time, ad_time)
    browser.quit()
# 执行程序
while True:   
    
    # 当前小时
    now_hour = int(time.strftime("%H", time.localtime()))
    if now_hour >= sleep_start_hour and now_hour < sleep_stop_hour :
        writeLog('------------------------------------------')
        writeLog('休息时间为：'+ str(sleep_start_hour)+'点到' + str(sleep_stop_hour) +'点,正在休息')    
        time.sleep(calSleepTime(sleep_stop_hour))
    else:
         # 每小时更新一次数据
        if now_hour != now_update_hour :
            # 获得URL
            data_list = getUrlList()
            now_update_hour = now_hour
            writeLog('------------------------------------------')
            writeLog('获得当天'+ str(now_update_hour) +'点数据')
            
        count += 1
        writeLog('---------第'+ str(count) +'次访问---------------')
        runTask(data_list, open_min_time,open_max_time,ad_min_time,ad_max_time)
        rest_time = random.randint(rest_min_time, rest_max_time)
        writeLog('执行间隔：'+ str(rest_time))
        time.sleep(rest_time)
    
       
    