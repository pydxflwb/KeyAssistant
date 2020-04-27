from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
import requests
from aip import AipOcr
import json


def get_captcha(captcha_url, cookies, params):
    response = requests.get(captcha_url, cookies=cookies, params=params)
    with open('img.jpeg', 'wb+') as f:
        f.writelines(response)


APP_ID = '19280131'
API_KEY = 'rCZqiVMgCtF3mTwTnoCjqpIw'
SECRET_KEY = 'AkFtdaibGa5MNcgpqIxa94pS9EO8r6KZ'


def browser_access_monitor(browser, url, captcha_url, excepted_url, user, pswd):
    access_flag = False
    while not access_flag:
        # try:
        browser.get(url)
        cookies = browser.get_cookies()
        cookies = {i["name"]: i["value"] for i in cookies}
        uuid = browser.find_element_by_xpath('//form/input[@name="uuid"]')
        params = {
            'uuid': uuid.get_attribute('value')
        }
        get_captcha(captcha_url, cookies, params)
        with open('img.jpeg', 'rb') as fp:
            image = fp.read()
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        raw_code = client.accurate(image)
        code0 = raw_code['words_result'][0]
        code0 = code0['words'].split(' ')
        code = ''
        for c in code0:
            code = code + c
        print(code)
        fp.close()
        input_user = browser.find_element_by_id('user')
        input_user.send_keys(user)
        input_pass = browser.find_element_by_id('pass')
        input_pass.send_keys(pswd)
        input_code = browser.find_element_by_id('captcha')
        input_code.send_keys(code)
        input_code.send_keys(Keys.ENTER)
        if excepted_url in browser.current_url:
            access_flag = True
        # except:
        #     print("Something Wrong")
    return browser.current_url


def get_curricular(browser, url, waittime):
    browser.get(url)
    wait = ui.WebDriverWait(browser, waittime)
    wait.until(lambda driver: browser.find_element_by_id('kbgrid_table_0'))
    curri_table = browser.find_element_by_id('kbgrid_table_0')
    result = []
    curri_lists = curri_table.find_elements_by_tag_name('tr')
    counter = 0
    for i in range(len(curri_lists)):
        if i > 1:
            curri_rows = curri_lists[i]
            # print(curri_rows)
            curri_result = []
            curri = curri_rows.find_elements_by_tag_name('td')
            for j in range(len(curri)):
                if j > 0:
                    curriculum = curri[j]
                    try:
                        single_result = []
                        curri_details = curriculum.find_element_by_tag_name('div')
                        curri_name = curri_details.find_element_by_class_name('title')
                        single_result.append(curriculum.get_attribute("id"))
                        single_result.append(curri_name.text)
                        curri_other_details = curri_details.find_elements_by_tag_name('p')
                        for det in curri_other_details:
                            single_result.append(det.text)
                        counter += 1
                        curri_result.append(single_result)
                    except:
                        pass
            result.append(curri_result)
    browser.close()
    return json.dumps(result)


def store_curricular_data(curri_data, file):
    curri_data = json.loads(curri_data)
    if curri_data is None:
        print("No File !")
    else:
        display_result = []
        for curri_line in curri_data:
            if curri_line:
                for curri in curri_line:
                    try:
                        room_data = curri[7].split("会议号")[1]  # 这句提前用于验证try

                        display_curri = []
                        display_curri.append(curri[1])  # 课程名 curri name
                        curri_num = curri[5].split(")")[1]
                        curri_num = curri_num.split("-")[1]
                        display_curri.append(curri_num)  # 课号 curri number
                        display_curri.append(curri[4])  # 教师 teacher
                        display_curri.append(curri[0][0])  # 周内时间(数字) curri week day
                        display_curri.append(curri[2])  # 时间段 curri timespan
                        display_curri.append(curri[-1])  # 学分 credit

                        room_num = room_data.split("；")[0]
                        room_num = room_num.split("：")[1]
                        display_curri.append(room_num)  # 会议号 room number
                        room_pswd = room_data.split("；")[1]
                        room_pswd = room_pswd.split("：")[1]
                        display_curri.append(room_pswd)  # 会议密码 room password

                        display_result.append(display_curri)
                    except IndexError:
                        pass
                    # else:
                    #     print("Other Error Occurs!")
                    #     pass

        # Sort
        length = len(display_result)
        for i in range(length):
            for j in range(1, length - i):
                if display_result[j-1][3] > display_result[j][3]:
                    display_result[j], display_result[j-1] = display_result[j-1], display_result[j]
                else:
                    if display_result[j-1][3] == display_result[j][3]:
                        if display_result[j-1][4][1] > display_result[j][4][1]:
                           display_result[j], display_result[j - 1] = display_result[j - 1], display_result[j]

        with open(file, "w") as f:
            f.write(json.dumps(display_result))
        f.close()


time_dict = {1:[7,45], 2:[8,40], 3:[9,45], 4:[10,40], 5:[11,45], 6:[12,40],
             7:[13,45], 8:[14,40], 9:[15,45], 10:[16,40],
             11:[17,45], 12:[18,40], 13:[19,45], 14:[20,20]}


def create_time_json(file, ofile):
    with open(file, 'r') as f:
        raw_curri = json.load(f)
    f.close()
    default_time = []
    for curri in raw_curri:
        curri_timesetting = []
        curri_timesetting.append(curri[1])  # 课号
        curri_timesetting.append(curri[3])  # 周内时间
        start = curri[4].split('-')[0][-1]
        end = curri[4].split('-')[1][0]
        for key in time_dict:
            if int(start) == key:
                curri_timesetting.append(time_dict[key])
            if int(end)+1 == key:
                curri_timesetting.append(time_dict[key])
        default_time.append(curri_timesetting)
    with open(ofile, 'w') as of:
        of.write(json.dumps(default_time))
    of.close()


def change_DataStyle_List(file, timefile):
    with open(file, 'r') as f:
        raw_curri = json.load(f)
    f.close()
    with open(timefile, 'r') as tfi:
        timedata =json.load(tfi)
    tfi.close()
    curri_liststyle = []
    for curri in raw_curri:
        curri_new = []
        curri_new.append(curri[0][:-1]+'  '+curri[1]+'\n'+curri[2])  # 课程信息(简略) Some Data
        curri_new.append('周'+curri[3]+' '+curri[4])  # 课程时间 curri time
        curri_new.append('会议号:'+curri[6]+'\n密码:'+curri[7])  # 会议信息
        for time in timedata:
            if time[0] == curri[1] and time[1] == curri[3]:
                curri_new.append(str(time[2][0])+':'+str(time[2][1])+'--'
                                 +str(time[3][0])+':'+str(time[3][1]))
        curri_new.append(curri[0][-1])  # 课程类型 curri type
        curri_liststyle.append(curri_new)
    return curri_liststyle


kbcx_url = "http://kbcx.sjtu.edu.cn/jaccountlogin"
sjtu_captcha_url = "https://jaccount.sjtu.edu.cn/jaccount/captcha"
username = ''
password = ''
url1 = "http://kbcx.sjtu.edu.cn/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N2151&layout=default"
sjtu_excepted_url = "http://kbcx.sjtu.edu.cn/xtgl/index_initMenu.html"
file1 = "../settings/curricular.json"
file2 = "../settings/time_setting.json"

if __name__ == "__main__":
    webbrowser = webdriver.Chrome()
    new_url = browser_access_monitor(webbrowser, kbcx_url,
                                   sjtu_captcha_url, sjtu_excepted_url, username, password)
    data = get_curricular(webbrowser, url1, 10)
    store_curricular_data(data, file1)
    create_time_json(file1, file2)
    change_DataStyle_List(file1, file2)

    # print(json.dumps("◇-\u25c7理论  ●-\u25cf实验  ○-\u25cb实习  ★-\u2605上机  ▲-\u25b2其他  ☆-\u2606课程设计"))

