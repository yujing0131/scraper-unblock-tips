from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
import time
import base64  #進行圖片編碼的處理

##爬取網頁一般驗證碼的圖片
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://cart.books.com.tw/member/login?loc=customer_003&url=https%3A%2F%2Fwww.books.com.tw%2F')
time.sleep(5)

#由於使用requests下載驗證碼圖片時會自動產生新的圖片，因此要使用selenium excute利用javascript來繪製圖片
img_base64 = browser.execute_script("""
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = ele.width; cnv.height = ele.height;
    cnv.getContext('2d').drawImage(ele, 0, 0);
    return cnv.toDataURL('image/jpeg').substring(22);
""",browser.find_element(By.ID,'captcha_img').find_element(By.TAG_NAME,'img')##搜尋ID為"captcha_img"下面的DIV元素

)
##建立檔案物件將編碼字串的圖片寫入二進位碼檔案完成下載的動作
with open('captacha.png','wb') as image:#指定為
    #將編碼圖片的編碼碼字串解碼然後寫入檔案
    image.write(base64.b64decode(img_base64))
##傳送網頁一般驗證碼的圖片到2Captcha服務(需要註冊以及付費)
api_key = ''

##傳送到指定的API解碼網址https://2captcha.com/in.php
##定義一個字典變數準備驗證碼圖片
file = {'file':open('captacha.png','rb')}
data = {
    'key':api_key,
    'method':'post'
        }
response = requests.post('https://2captcha.com/in.php',files=file,data=data)

captcha_id = response.text.split('|')[1]
#將取得captcha_id和api_key傳送到指定網址取得驗證碼字串
##取得網頁一般驗證碼的辨識結果，由於驗證碼圖片無法一次就辨識出來，所以利用for迴圈重複執行呼叫的動作

for i in range(10):
    result= requests.get(f'https://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}')
    #如果回應結果為CAPCHA_NOT_READY舊代表還沒有辨識完成
    if result.text.find('CAPCHA_NOT_READY')> -1:
        time.sleep(5)
    elif result.text.find('OK') > -1:
        captcha_text = result.text.split('|')[1]
        break
    else:
        print('發生錯誤!')

#在輸入驗證碼欄位填入辨識結果
browser.find_element(By.ID,'captcha').send_keys(captcha_text)
time.sleep(10)
