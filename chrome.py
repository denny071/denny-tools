'''
后台自动化登录
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from time import sleep  # 导入等待 无比重要的等待


def initChrome():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(
        options=options, executable_path=r'/usr/local/bin/chromedriver')
    browser.maximize_window()    # 最大化页面
    return browser


def login(browser, url, username, password):
    browser.get(url)
    browser.find_element_by_name("username").send_keys(username)
    browser.find_element_by_name("password").send_keys(password)
    browser.find_element_by_id("btnSubmit").click()

 
# 创建内容窗口
def contentCreate(browser,FrameName):
    browser.switch_to.frame(browser.find_element_by_name(FrameName))
    browser.find_element_by_css_selector("#toolbar > .btn-primary").click()
    browser.switch_to.frame(browser.find_element_by_name("layui-layer-iframe1"))
    
# 新闻内容创建
def newsContentCreate(browser):
    	
	Select(browser.find_element_by_name("categoryId")).select_by_visible_text("汽车内容")
	sleep(2)
	for input in browser.find_elements_by_tag_name('input[type=checkbox]'):
		input.click()
	browser.find_element_by_name("title").send_keys("睡沙发还舒服的底盘")
	browser.find_element_by_name("titleSecond").send_keys("如何打造比睡沙发还舒服的底盘？了解完东风雪铁龙天逸后我懂了")
	browser.find_element_by_name("author").send_keys("测试人员")
	browser.find_element_by_id("file").send_keys("/Users/denny/Documents/GitHub/test.png")
	browser.execute_script("window.editor.insertHtml('日前，车视界分析了2020年11月中国品牌SUV销量，排行榜TOP5正式出炉。')");
	sleep(2)
	browser.find_element_by_id("submitData").click()
	
def contentModify(browser):
	browser.switch_to.frame(browser.find_element_by_name("iframe25"))
	button = browser.find_element_by_css_selector(".btn-warning")
	print(button)
	browser.switch_to.frame(browser.find_element_by_name("layui-layer-iframe1"))

# 打开菜单
def menu(menuName, subMenuName):
    for menu in browser.find_element_by_tag_name(name='nav').find_elements_by_tag_name(name='a'):
        if (menu.text == menuName or menu.text == subMenuName):
            menu.click()


def close(browser):
    browser.quit()



browser = initChrome()
login(browser,"http://127.0.0.1/login","root","root")
sleep(5)
menu("内容管理", "文章内容")
sleep(10)
contentCreate(browser,"iframe25")
newsContentCreate(browser)
# contentModify(browser)
# videoContentCreate(browser)


sleep(5)
# close(browser)
