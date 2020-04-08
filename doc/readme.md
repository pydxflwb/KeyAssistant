# 一键网课助手

* [English Readme File](http://github.com/pydxflwb/KeyAssistant/tree/master/doc/readme_en.md)

_一键网课助手_ 是一个帮助SJTU学生快速登录Zoom平台含密码会议室的程序


 2020.04.08:  __这个程序的一期功能代码已经上传！__
            
            当前demo版本尚未提供安装和使用功能。
            仅作为开发和测试使用            
 
 
 ## 运行环境及库依赖
 （目前仅适用于Windows 10系统，使用Mac的同学实在抱歉）
 * Python 3.5, 3.6, 3.7（推荐3.6.x）
 * selenium	3.141.0
 * requests	2.23.0	 
 * PyQt5 5.13.x以上，及对应pyqt5tools
 * baidu-aip (百度提供的OCR接口)
 * Pywin32
 * pyautogui
 * pyHook(Python 3版本可能需要.whl)
 * pyUserInput
 
 ## 安装
 * Chrome浏览器需要Chrome driver。在Chrome网址栏中输入[Chrome://version](Chrome://version)查看版本，在
 [Chrome Driver下载地址](http://chromedriver.storage.googleapis.com/index.html)下载对应版本（最接近）的Driver，
并将其路径加入系统变量Path。（Selenium默认支持Firefox，IE/Edge/Chrome需安装对应driver）

 
 ## 功能介绍
 
 ### 再也不怕早起手忙脚乱！不需要到处找房间号和密码！
 * 一键登录当前时间对应的课程Zoom会议室！
 * 可以自己设置每门课对应的时间，在时间段内点击一键上课都是这节课哦！
  
 ## 使用说明
 
 
 
 ## 联系作者
 肖 鹏宇  (pydxflwb@sjtu.edu.cn)
 欢迎提交issue! 欢迎使用和改进！
 
 本文档最近更新日期: April 8 2020
 