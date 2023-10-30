import requests
import json

response = requests.get("https://www.twse.com.tw/rwd/zh/afterTrading/BWIBBU_d?date=20230912&selectType=30&response=json&_=1694572541598")
print(response.json()['data'])##爬取網頁所有股票的陣列資料
print(response.json()['data'][1])##只有爬取第2筆股票陣列資料