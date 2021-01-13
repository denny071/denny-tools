from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


'''
东行记Port自动测试
'''

testUrl="http://120.92.116.180/dxj/html/index.html"

hotNewsList = [
    "/html/body/div/section/div[1]/ul/li[1]/a/span",
    "/html/body/div/section/div[1]/ul/li[2]/a/span",
    "/html/body/div/section/div[1]/ul/li[3]/a/span",
    "/html/body/div/section/div[1]/ul/li[4]/a/span"
]


hotRecommandList = [
    "/html/body/div/section/div[5]/div[5]/div[1]/div/div/div/a/h5",
    "/html/body/div/section/div[5]/div[5]/div[2]/div/div/div/a/h5",
    "/html/body/div/section/div[5]/div[5]/div[3]/div/div/div/a/h5",
    "/html/body/div/section/div[5]/div[5]/div[4]/div/div/div/a/h5",
]


allNewsButton = "/html/body/div/section/div[1]/div/a"
allNewsList = [
    "/html/body/div/div/section/ul/li[5]/a/h4",
    "/html/body/div/div/section/ul/li[6]/a/h4",
    "/html/body/div/div/section/ul/li[7]/a/h4",
    "/html/body/div/div/section/ul/li[8]/a/h4",
]

def showLog(conent):
    print("[INFO] " + conent)
    
def showErrorLog(conent):
    print("[ERROR] " + conent)
    
def goback(driver):
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div/nav/h1/span').click()
    time.sleep(2)


def checkHotNews(xpath):
    try:
        list_title = driver.find_element_by_xpath(xpath).text
    except Exception:
        showErrorLog(driver.current_url + "：列表异常")
    else: 
        showLog("列表标题为："+ list_title)
        driver.find_element_by_xpath(xpath).click()
        time.sleep(2)
        
    try:
        content_title = driver.find_element_by_tag_name('h2').text
    except Exception:
        showErrorLog(driver.current_url + "：内容异常")
    else:
        showLog("内容标题为："+ content_title)
        if list_title == content_title:
            showLog(driver.current_url + "：标题一致")
        else:
            showErrorLog(driver.current_url + "：标题不一致")
    goback(driver)
    
   
def checkHotRecommand(xpath):
    try:
        list_title = driver.find_element_by_xpath(xpath).text
    except Exception:
        showErrorLog(xpath + "：列表异常")
    else: 
        showLog("列表标题为："+ list_title)
        driver.find_element_by_xpath(xpath).click()
        time.sleep(2)
        
    try:
        content_title = driver.find_element_by_tag_name('h2').text
    except Exception:
        showErrorLog(driver.current_url + "：内容异常")
    else:
        showLog("内容标题为："+ content_title)
        if list_title == content_title:
            showLog(driver.current_url + "：标题一致")
        else:
            showErrorLog(driver.current_url + "：标题不一致")
    goback(driver)
 
 
options = webdriver.ChromeOptions()
options.add_experimental_option('mobileEmulation', {'deviceName': 'iPhone X'})
driver = webdriver.Chrome(options=options)
driver.get(testUrl)
time.sleep(6)




# # 首页顶部新闻
# for item in hotNewsList:
#     checkHotNews(item)

# 全部新闻
# driver.find_element_by_xpath(allNewsButton).click()
# time.sleep(2)
# for item in allNewsList:
#     checkHotNews(item)
# goback(driver)

# # 热门推荐
offset=1400 
for item in hotRecommandList:
    driver.execute_script("window.scrollBy(0,"+str(offset)+")")    
    time.sleep(3)
    checkHotRecommand(item)
    offset=offset+300
    


# goback(driver)
# time.sleep(3)
# driver.find_element_by_xpath('/html/body/div/section/div[1]/ul/li[2]/a/span').click()
# goback(driver)
# time.sleep(3)
# driver.find_element_by_xpath('/html/body/div/section/div[1]/ul/li[3]/a/span').click()
# goback(driver)
# time.sleep(3)
# driver.find_element_by_xpath('/html/body/div/section/div[1]/ul/li[4]/a/span').click()
# goback(driver)
 # 