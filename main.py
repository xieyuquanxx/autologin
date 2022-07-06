import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

from PIL import Image
import requests
import base64


def get_access_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=0Fg3VTCGUaHBToIl9uOTAFtQ&client_secret=Wal7gicPWuD1TGkY9OIFTzaLET8Nl06C'
    response = requests.get(host)
    if response:
        print(response.json())

    # "access_token": "24.f3edd87a886bb217b6ebbf8989fafdc2.2592000.1659531895.282335-26623131",


def get_captcha():
    # 获取验证码
    captcha_id = "img_verify"
    png = browser.find_element(By.ID, captcha_id)
    png.screenshot("capt.png")
    img = Image.open("capt.png").convert("L")  # P转换为L模式
    count = 102  # 设定阈值
    table = []
    for i in range(256):
        if i < count:
            table.append(0)
        else:
            table.append(1)

    img = img.point(table, '1')
    img.save('captcha1.png')  # 保存处理后的验证码

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    f = open("captcha1.png", 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = "24.f3edd87a886bb217b6ebbf8989fafdc2.2592000.1659531895.282335-26623131"
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        text = str(response.json())
        print(text)
        text = text[:text.find(',')].replace("'", '"') + '}'
        data = json.loads(text)
        words = data['words_result'][0]['words'].replace(" ", '')
        return words


def input_info():
    # print(words)
    # 身份证选择框
    select_id = "select_certificate"
    select_element = browser.find_element(By.ID, select_id)
    select_object = Select(select_element)
    select_object.select_by_index(1)
    # 身份证号
    card_id = "input_idCardNo"
    input_card = browser.find_element(By.ID, card_id)
    ID = "H60115682"
    input_card.send_keys(ID)
    # 密码
    pwd_id = "input_pwd"
    input_pwd = browser.find_element(By.ID, pwd_id)
    PWD = "ISBN705608"
    input_pwd.send_keys(PWD)

    # 输入验证码
    words = get_captcha()
    captcha_id = "input_verifyCode"
    input_captcha = browser.find_element(By.ID, captcha_id)
    input_captcha.send_keys(words)


if __name__ == '__main__':
    browser = webdriver.Chrome()
    url = "https://hk.sz.gov.cn:8118/userPage/login"
    browser.get(url)
    try:
        # 进来有个提示框
        btn = browser.find_element(By.ID, "winLoginNotice").find_element(By.CLASS_NAME, "flex1").find_element(
            By.TAG_NAME,
            "button")
        btn.click()

        input_info()

        # 登录按钮
        login_id = "btn_login"
        login_btn = browser.find_element(By.ID, login_id)
        login_btn.click()

        time.sleep(0.1)

        # 进来有个提示框
        btn = browser.find_element(By.ID, "winOrderNotice").find_element(By.CLASS_NAME, "flex1").find_element(
            By.TAG_NAME,
            "button")
        btn.click()

        # 点击我要预约按钮
        order_id = "a_canBookHotel"
        order_btn = browser.find_element(By.ID, order_id)
        order_btn.click()

        # 进来后找到预约按钮
        cards = browser.find_elements(By.CLASS_NAME, "card_info")
        for card in cards:
            card_btn = card.find_element(By.TAG_NAME, "button")
            # print(card_btn)
            card_btn.click()
    except NoSuchElementException:
        browser.quit()

    # 退出
    # browser.quit()
