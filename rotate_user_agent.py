import requests
import json
import random
import re
from bs4 import BeautifulSoup  

#建立多組User Agent清單
response = requests.get('https://www.useragentstring.com/pages/Chrome/')
soup = BeautifulSoup(response.text,'lxml')
user_agents = soup.find_all('li')
User_Agent=[]
for user_agent in user_agents:
    User_Agent.append(user_agent.text)
    
#隨機選擇一組User Agent發送請求
user_agent = random.choice(User_Agent)

#將隨機選擇的User Agent夾帶在請求的標頭header裡面
header = {
    'User-Agent':user_agent
}
response = requests.get("https://www.twse.com.tw/rwd/zh/afterTrading/BWIBBU_d?date=20230912&selectType=30&response=json&_=1694572541598",
                        headers=header)
print(response.json()['data'])##爬取網頁所有股票的陣列資料
print(response.json()['data'][1])##只有爬取第2筆股票陣列資料