from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random
from selenium.common import exceptions

def taobao_login():
    login_url = 'https://login.taobao.com'
    drive = webdriver.Firefox()
    drive.maximize_window()
    wait = WebDriverWait(drive, 20)

    drive.get(login_url)
    click = wait.until(EC.element_to_be_clickable((By.XPATH, '//i[@class="iconfont static"]')))
    click.click()

    input_password(drive)
    time.sleep(1)
    # time.sleep(0.01)
    need_agin = ' '
    while need_agin:
        time.sleep(0.5)
        try:
            need_agin = drive.find_element_by_xpath('//*[@id="J_Message"]/p')
            print('need_agin:', need_agin)
        except:
            print('found')
            need_agin = ''
            break
        if '滑块' in need_agin.text:
            retry = 0
            while retry < 5:
                print('retry:',retry)
                retry += 1
                input_QR(drive)
        else:
            input_password(drive)

    time.sleep(1)
    title = drive.title
    cur_url = drive.current_url
    cookies = drive.get_cookies()
    print('cookies:', cookies)
    print('title:', title)
    print('cur_url:', cur_url)
    # password_text = drive.find_element_by_xpath('//input[@="TPL_password_1"]')

def input_QR(drive):
    slider = drive.find_element_by_xpath('//*[@id="nc_1_n1z"]')
    slider_rect = drive.find_element_by_xpath('//*[@id="nc_1__scale_text"]')
    print(slider_rect)
    if slider:
        x = slider.location.get('x')
        y = slider.location.get('y')
        width = slider_rect.rect.get('width')
        print('width:', width)
        list_track = slider_track(width)
        # ActionChains(drive).drag_and_drop_by_offset(slider, x + width*4/5, y).perform()
        action = ActionChains(drive)
        action.click_and_hold(slider)
        for track in list_track:
            action.move_by_offset(track, 0)
        # action.move_by_offset(258, 0)
        action.perform()
        action.reset_actions()
        # while list_track:
        #     x = random.choice(list_track)
        #     action.move_by_offset(x, 0).perform()
        #     list_track.remove(x)
        # action.release().perform()
        time.sleep(1)
        try:
            slide_refresh = drive.find_element_by_xpath("//div[@id='nocaptcha']/div/span/a")  # 页面没有滑块，而是“点击刷新再来一次”
            slide_refresh.click()
        except exceptions.NoSuchElementException:  # 滑动成功
            print('ok')
            return
        # try:
        #     check_slider = drive.find_element_by_xpath('//span[@class="nc-lang-cnt" and @data-nc-lang="_yesTEXT"]/p').text
        # except:
        #     input_password(drive)
        # if '验证通过' in check_slider:
        #     input_password(drive)


def slider_track(width):
    mid_pos = (4/5) * width
    # mid_pos = width +100
    a1 = 50
    a2 = -80
    v = 0
    current_pos = 0
    list_track = []
    #at
    #v0t + 1/2at2
    t = 0.5
    while current_pos < width:
        if current_pos < mid_pos:
            a = a1
        else:
            a = a2

        v0 = v
        v = v0 + a * t
        move = v0 * t + (1 / 2) * a * t * t
        current_pos += move

        list_track.append(move)

    return list_track

def input_password(drive):
    username = input('username:')
    password = input('password:')

    username_text = drive.find_element_by_xpath('//input[@id="TPL_username_1"]')
    username_text.clear()
    username_text.send_keys(username)
    # time.sleep(0.5)

    password_text = drive.find_element_by_xpath('//input[@id="TPL_password_1"]')
    password_text.clear()
    password_text.send_keys(password)
    # time.sleep(0.5)
    #为了你的账户安全，请拖动滑块完成验证
    #你输入的密码和账户名不匹配，是否忘记密码或忘记会员名
    login = drive.find_element_by_xpath('//button[@id="J_SubmitStatic"]')
    login.click()
def main():
    taobao_login()

if __name__ == '__main__':
    main()