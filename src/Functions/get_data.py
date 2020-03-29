from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
import requests
import pytesseract
from PIL import Image

browser = webdriver.Chrome()

url = "http://kbcx.sjtu.edu.cn/jaccountlogin"
captcha_url = "https://jaccount.sjtu.edu.cn/jaccount/captcha"
user = 'pydxflwb'
pswd = '19990904xpyu'


def get_captcha(captcha_url, cookies, params):
    response = requests.get(captcha_url, cookies=cookies, params=params)
    with open('img.jpeg', 'wb+') as f:
        f.writelines(response)

try:
    browser.get(url)
    cookies = browser.get_cookies()
    cookies = {i["name"]: i["value"] for i in cookies}
    uuid = browser.find_element_by_xpath('//form/input[@name="uuid"]')
    params = {
        'uuid': uuid.get_attribute('value')
    }
    get_captcha(captcha_url, cookies, params)
    image = Image.open('img.jpeg')
    code = pytesseract.image_to_string(image)
    print(code)
    input_user = browser.find_element_by_id('user')
    input_user.send_keys(user)
    input_pass = browser.find_element_by_id('pass')
    input_pass.send_keys(pswd)
    input_code = browser.find_element_by_id('captcha')
    input_code.send_keys(code)
    input_code.send_keys(Keys.ENTER)
    print(browser.current_url)
    url1 = "http://kbcx.sjtu.edu.cn/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N2151&layout=default"
    browser.get(url1)
    wait = ui.WebDriverWait(browser, 10)
    wait.until(lambda driver: browser.find_element_by_id('kbgrid_table_0'))
    curri_table = browser.find_element_by_id('kbgrid_table_0')
    print(curri_table)

finally:
    print('success!')



# try:
# kbcx = browser.find_element_by_xpath("//*[contains(@onclick,'学生课表查询')]")
# print(kbcx)
# kbcx.click()
# except:
#     print("error")



# wait.until(curri_table.find_element_by_id('kbgrid_table_0'))


result = []
curri_lists = curri_table.find_elements_by_tag_name('tr')
for i in len(curri_lists):
    if i > 1:
        curri_rows = curri_lists[i]
        print(curri_rows)
        curri_result = []
        curri = curri_rows.find_elements_by_tag_name('td')
        for j in len(curri):
            
#     curri_data = curri.find_element_by_tag_name('td')
