from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip119/queryTime')
browser.find_element(By.ID,'startStation').send_keys('3360-彰化')
browser.find_element(By.ID,'endStation').send_keys('5000-屏東')

api_key = ''
id="recaptcha-anchor"
##將key2替代為api_key、googlekey替代為data-sitekey值、pageurl設定為台鐵剩餘座位查詢網址、以及設定使用的2captcha服務的API版本為enterprise=1代表使用enterprise版本
response = requests.get(f'https://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey=6LdHYnAcAAAAAI26IgbIFgC-gJr-zKcQqP1ineoz&pageurl=https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip119/queryTime&enterprise=1')

captacha_id = response.text.split("|")[1]
for i in range(10):
    result = requests.get(f'https://2captcha.com/res.php?key={api_key}&action=get&id={captacha_id}')
    if result.text.find('CAPCHA_NOT_READY')> -1:
        time.sleep(10)
    #若
    elif result.text.find('OK') > -1:
        captcha_text = result.text.split('|')[1]
        break
    else:
        print('發生錯誤!')

#將取得的辨識結果認證碼回填到網頁上，呼叫execute_script語法執行javascript程式碼
browser.execute_script('document.getElementById("g-recaptcha-response").innerHTML="[0]";',captcha_text)
##captcha協助突破圖片辨識碼後點擊查詢
browser.find_element(By.ID,'searchButton').click()
time.sleep(10)