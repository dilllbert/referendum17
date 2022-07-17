import pathlib
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def getid():
    url = "https://referendum.2021.nat.gov.tw/pc/zh_TW/js/option.js"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'}

    res = requests.get(url,headers=headers) 
    soup = BeautifulSoup(res.text,'html.parser') 
    soup = str(soup)

    item_list = soup.split("case")[1:]
    
    id_list = []
    for item in item_list:
        id_list.append(str(item[2:12]))

    return id_list
    

def getinfo():
    
    option = Options()

    option.add_argument("--headless")
    option.add_argument("--disable-notifications")
    option.add_argument('blink-settings=imagesEnabled=false')
    
    driverpath='geckodriver.exe'
    
    driver = webdriver.Firefox(executable_path=driverpath,options=option)
    av = []     #同意票數
    nav = []    #不同意票數
    vv = []     #有效票數
    nvv = []    #無效票數
    vc= []      #投票數
    vpc=[]      #投票權人數
    avp=[]      #已完成投票所投票率(%)
    vv2vpc=[]   #有效同意票數對投票權人數(%)
    dist = []   #行政區
    County = [] #縣市

    url = 'https://referendum.2021.nat.gov.tw/pc/zh_TW/01/{}0000000.html'

    id_list = getid()

    for id in id_list:
            driver.get(url.format(id))
            rawinfo =  driver.find_element(By.XPATH, '//*[@id="divContent"]/table/tbody/tr[1]/td[2]/b').get_attribute('textContent')

            if '縣' in rawinfo:
                County += [rawinfo[rawinfo.index('縣')-3:rawinfo.index('縣')+1]]
                dist += [rawinfo[rawinfo.index('縣')+1:]]
            else :
                County += [rawinfo[rawinfo.index('市')-3:rawinfo.index('市')+1]]
                dist += [rawinfo[rawinfo.index('市')+1:]]

            av +=       [driver.find_element(By.XPATH, '//*[@id="divContent"]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[1]').get_attribute('textContent')]
            nav+=       [driver.find_element(By.XPATH, '//*[@id="divContent"]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]').get_attribute('textContent')]
            vv +=       [driver.find_element(By.XPATH, '//*[@id="divContent"]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[3]').get_attribute('textContent')]
            nvv +=      [driver.find_element(By.XPATH, '//*[@id="divContent"]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[4]').get_attribute('textContent')]
            vc +=       [driver.find_element(By.XPATH, '//*[@id="divContent"]/table/tbody/tr[4]/td/table/tbody/tr[5]/td[1]').get_attribute('textContent')]
            vpc +=      [driver.find_element(By.XPATH, '//*[@id="divContent"]/table/tbody/tr[4]/td/table/tbody/tr[5]/td[2]').get_attribute('textContent')]
            avp +=      [driver.find_element(By.XPATH, '//*[@id="divContent"]/table/tbody/tr[4]/td/table/tbody/tr[5]/td[3]').get_attribute('textContent')]
            vv2vpc +=   [driver.find_element(By.XPATH, '//*[@id="divContent"]/table/tbody/tr[4]/td/table/tbody/tr[5]/td[4]').get_attribute('textContent')]

    voteinfo ={    
        '縣市' :County,
        '行政區':dist,
        '同意票數':av,
        '不同意票數':nav,
        '有效票數':vv,
        '無效票數':nvv,
        '投票數':vc,
        '投票權人數':vpc,
        '已完成投票所投票率(%)':avp,
        '有效同意票數對投票權人數(%)':vv2vpc
    }

    voteinfo_df = pd.DataFrame(voteinfo)

    try:
        voteinfo_df.to_csv(str(pathlib.Path(__file__).parent.absolute())+"//title.csv",encoding='utf_8_sig',index = False)
    except:
        print("123")


getinfo()

