import os, time, datetime
import json
import win32gui, win32con
import pyautogui as auto
from pykeyboard import PyKeyboard


def auto_openzoom(zoomlink):
    if not zoomlink:
        zoomlink = os.path.join(os.path.expanduser('~'), "Desktop\\Zoom.lnk")
    os.startfile(zoomlink)
    procHandler = None
    for i in range(30):
        if not procHandler:
            procHandler = win32gui.FindWindow(None, "Zoom")
            if procHandler:
                win32gui.ShowWindow(procHandler, win32con.SW_SHOW)
                break
        time.sleep(1)

    # time.sleep(2)
    # win32gui.ShowWindow(procHandler, win32con.SW_HIDE)


def zoom_auto(pic_dir, roomnum, password):
    try:
        k = PyKeyboard()
        mouse = auto.locateCenterOnScreen(pic_dir)
        auto.click(x=mouse.x, y=mouse.y, clicks=1, button='left')
        time.sleep(1)
        k.type_string(roomnum)
        k.tap_key(k.enter_key)
        time.sleep(3)
        k.type_string(password)
        k.tap_key(k.enter_key)
        return True
    except:
        return False


def zoom_signin(zoomlink, pic_dir, roomnum, password):
    auto_openzoom(zoomlink)
    for i in range(10):
        time.sleep(2)
        flag = zoom_auto(pic_dir, roomnum, password)
        print(i+1)
        if flag:
            return True
    return False


def signin_nowtime(pic_dir, file, timefile, weekday, nowtime):
    classdata, roomnum, password = showcurri_now(file, timefile, weekday, nowtime)
    if roomnum and password:
        flag0 =zoom_signin('', pic_dir,roomnum, password)
        if flag0:
            return 1
        else:
            return -1
    else:
        print("No")
        return 0


def showcurri_now(file, timefile, weekday, nowtime):
    classdata=''
    roomnum=''
    password=''
    with open(file) as f:
        raw_curri = json.load(f)
    f.close()
    with open(timefile) as tif:
        raw_time = json.load(tif)
    tif.close()
    for time0 in raw_time:
        if weekday == int(time0[1]):
            if nowtime[0] > time0[2][0] or (nowtime[0] == time0[2][0] and nowtime[1] >= time0[2][1]):
                if nowtime[0] < time0[3][0] or (nowtime[0] == time0[3][0] and nowtime[1] < time0[3][1]):
                    for curri in raw_curri:
                        if curri[1] == time0[0] and int(curri[3]) == weekday:
                            roomnum = curri[6]
                            password = curri[7]
                            classdata = curri[0]+' '+curri[4]
    return classdata, roomnum, password


# if __name__ == "__main__":
#     file1 = "../settings/curricular.json"
#     file2 = "../settings/time_setting.json"
#     pic = "../settings/1.png"
#     signin_nowtime(pic, file1, file2, 3, [9, 5])
