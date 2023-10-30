import requests
import json
import random
import re  #引用正規表達是來表達IP格式快速爬取網頁上的格式

#1.建立多組Proxy IP清單
response = requests.get('https://www.sslproxies.org/')

#\d+表示一位數以上的數字，尋找所有符合以下格式的IP為旨就會擷取出
proxy_ips = re.findall('\d+\.\d+\.\d+\.\d+:\d+',response.text)
# print(proxy_ips)

#2.驗證Proxy IP的有效性(並不是每一組ip每次都能使用，也有可能幾天後就無法使用)
vaild_ips = []
for proxy_ip in proxy_ips:
    try:
        ##不需要蒐集每一組有效IP，只需要蒐集五組，因此用IF判斷個數
        if len(vaild_ips) < 5:
            requests.get('https://ip.seeip.org/jsonip?',
                        proxies={'http':proxy_ip,'https':proxy_ip},#夾帶ip
                        timeout=10)#若10秒內有回應則表示該組ip有效，無效ip就要用try/except機制印出例外訊息
            #將有效的IP加入vaild_ips清單內
            vaild_ips.append(proxy_ip)
            
        else:
            break
    except:
        print(f"{proxy_ip}無效")


print(vaild_ips)
#3.隨機選擇一組Proxy IP 發送請求
ip = random.choice(vaild_ips)
print(f"隨機選擇{ip}")

#使用發送請求時夾帶隨機選擇的proxy ip降低網頁被偵測的風險
response = requests.get("https://www.twse.com.tw/rwd/zh/afterTrading/BWIBBU_d?date=20230912&selectType=30&response=json&_=1694572541598",
                        proxies={'http':ip,'https':ip})
print(response.json()['data'])##爬取網頁所有股票的陣列資料
print(response.json()['data'][1])##只有爬取第2筆股票陣列資料