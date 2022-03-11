import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from bs4 import BeautifulSoup
import datetime
import time
import base64


def format1(sample):
    guard = 0
    currenttime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    for i in sample:
        if i[-2:] == '00':
            temph = int(i[-5:-3])
            temph = temph - 1
            if len(str(temph)) == 1:
                temph = '0' + str(temph)
            else:
                temph = str(temph)
            temp = i[-16:-12] + i[-11:-9] + i[-8:-6] + temph + '59' + str(60 - lag)
        else:
            tempm = int(i[-2:])
            tempm = str(tempm - 1)
            if len(str(tempm)) == 1:
                tempm = '0' + str(tempm)
            else:
                tempm = str(tempm)
            temp = i[-16:-12] + i[-11:-9] + i[-8:-6] + i[-5:-3] + tempm + str(60 - lag)
        if int(currenttime) > int(temp):
            sample[guard] = '99999999999999'
        else:
            sample[guard] = temp
        guard = guard + 1

    return sample


def refresh():
    global soup, startList, linkList
    driver.get('https://spdpo.nottingham.edu.cn/study/selection')
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    soup = str(soup)
    start_pattern = re.compile('报名开始时间：.{16}')
    end_pattern = re.compile('报名结束时间：.{16}')
    place_pattern = re.compile('地点.*</div>')
    link_pattern = re.compile('/study/selection/activitydetail/.{36}')
    linkList_temp = link_pattern.findall(soup)
    linkList = []
    for i in linkList_temp:
        linkList.append("https://spdpo.nottingham.edu.cn" + i)
    startList_temp = start_pattern.findall(soup)
    startList = format1(startList_temp)


def main(link):
    guard = 0
    driver.get(link)
    while 1 > 0:
        time.sleep(0.8)
        driver.execute_script('onSelection()')
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH,
                            '//*[@id="layui-m-layer' + str(guard) + '"]/div[2]/div/div/div[2]/span[2]').click()
        guard += 3



def trigger():
    while 1 > 0:
        currenttime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        guard = 0
        for i in startList:
            if int(currenttime) >= int(i):
                main(linkList[guard])
        time.sleep(1)


lag = 10
account = ''
psword = ''

def log():
    global account, psword
    print('Version:Fuse0.1 Github repo:')
    if os.path.exists('Fuse_config.json'):
        f = open('Fuse_config.json', 'r')
        psword = base64.b64decode(f.readline()).decode()
        account = base64.b64decode(f.readline()).decode()

    else:
        account = str(input('账号plz\n'))
        psword = str(input('密码plz\n'))
        yn = input('保存密码？(y/n)#\n注意：Fuse仅会在本地进行简单加密，请勿在公共电脑使用此项功能\n')
        if yn == 'y' or yn == 'Y':
            print('正在保存密码...')
            try:
                byte_account = account.encode()
                byte_psword = psword.encode()
                f = open('Fuse_config.json', 'w')
                f.write(base64.b64encode(byte_psword).decode()+'\n'+base64.b64encode(byte_account).decode())
                f.close()
            except:
                print('保存失败...')





log()
driver = webdriver.Chrome()
driver.get("https://spdpo.nottingham.edu.cn/study/auth/Index?a=true")
driver.implicitly_wait(999)
driver.find_element(By.XPATH, '//*[@id="UserName"]').send_keys(account)
driver.find_element(By.XPATH, '//*[@id="Password"]').send_keys(psword)
driver.find_element(By.ID, 'btnLogin').click()


refresh()
trigger()


'''driver.execute_script('onSelection()')
driver.find_element(By.XPATH,'//*[@id="layui-m-layer0"]/div[2]/div/div/div[2]/span[2]').click()'''
# 2022-03-10 10:00