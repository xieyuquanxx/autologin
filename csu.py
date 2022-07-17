# 自动查询本学期的期末成绩
import base64
import json
import time

import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


# 获取验证码，发送百度apiOCR请求，并返回其验证结果
def get_captcha():
    captcha_id = "SafeCodeImg"
    png = browser.find_element(By.ID, captcha_id).screenshot("capt.png")
    img = Image.open("capt.png").convert("L")  # P转换为L模式
    count = 95  # 设定阈值
    table = []
    for i in range(256):
        if i < count:
            table.append(0)
        else:
            table.append(1)

    img.point(table, '1').save("captcha1.png")  # 保存处理后的验证码图像

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


# 输入用户名和密码
def input_info():
    account = "8208190106"
    password = "330326200106241818"

    browser.find_element(By.ID, "userAccount").send_keys(account)
    browser.find_element(By.ID, "userPassword").send_keys(password)

    words = get_captcha()
    print(f"验证码为{words}")

    browser.find_element(By.ID, "RANDOMCODE").send_keys(words)


# 点击我的成绩
def goto_score():
    ul = browser.find_element(By.ID, "divFirstMenuClass").find_element(By.TAG_NAME, "ul")
    ul.find_elements(By.TAG_NAME, "li")[2].click()


# 获取成绩表格
def get_score_table():
    table = browser.find_element(By.ID, "dataList")
    trs = table.find_elements(By.TAG_NAME, "tr")
    for tr in trs:
        print(tr.text)


if __name__ == '__main__':
    browser = webdriver.Chrome()
    url = "http://csujwc.its.csu.edu.cn/"
    browser.get(url)
    try:
        # 输入信息
        input_info()
        # 点击登录
        browser.find_element(By.ID, "btnSubmit").click()
        time.sleep(0.1)
        # 点击我的成绩
        # 吐槽：导航栏的a标签的id都一样，太差太差！
        goto_score()
        # browser.find_element(By.ID, "calender_user_schedule").click()
        # 选择学期
        select_element = browser.find_element(By.ID, "xnxq01id")
        select_object = Select(select_element)
        select_object.select_by_index(2)  # 默认选择本学期

        time.sleep(0.1)
        get_score_table()

        time.sleep(5)
        browser.quit()

    except Exception:
        browser.quit()
