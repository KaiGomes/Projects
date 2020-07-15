from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import time

driver = webdriver.Chrome("C:\\Users\\Kai Gomes\\Downloads\\chromedriver_win32\\chromedriver.exe")
actions = ActionChains(driver)
driver.set_page_load_timeout(10)
driver.get("https://howdy.tamu.edu")
driver.find_element_by_id("loginbtn").click()
driver.implicitly_wait(10)
driver.find_element_by_id("username").send_keys("kaigomes7")
driver.find_element_by_class_name("thinking-anim").click()
driver.find_element_by_id("password").send_keys("*Enter password here")
driver.find_element_by_class_name("thinking-anim").click()
time.sleep(10)
driver.get("https://howdy.tamu.edu/uPortal/p/TAMU-APP-Launcher.ctf1/detached/render.uP?pCm=view&pP_targetEndpoint=bwykfcls.p_sel_crse_search")
time.sleep(15)

while True:
    cap = driver.find_elements_by_class_name("dddefault")
    num = len(cap)
    j = []
    for i in range(num):
        j.append(cap[i].text)
        print(cap[i].text)
    if j[522] != '0' or j[862] != '0':
        os.startfile('Bell.mp3')
        break
    else:
        try:
            driver.refresh()
        except:
            os.startfile("Howdy.png")
            driver.refresh()
driver.implicitly_wait(5)


'''
    i = 1
    for ele in j:
        if ele == '22':
            l.append(ele)
    #print(l)
    print(len(l))
'''