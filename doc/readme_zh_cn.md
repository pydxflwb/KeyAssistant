# 一键网课助手

_一键网课助手_ 是一个帮助SJTU学生快速登录Zoom平台含密码会议室的程序

 这个程序正在开发中，敬请期待
 
 
 
 ### 运行环境及库依赖
 
 * Python 3.5, 3.6, 3.7（推荐3.6.x）
 * Scrapy 2.0.1
 (要求安装lxml, Twisted, Pywin32)
 * selenium	3.141.0
 * requests	2.23.0	 
 * PyQt5 5.13.x以上，及对应pyqt5tools
 * pytesseract 0.3.3
 
 ### 安装
 * 需要tesseract.exe。本程序中附带了3.2.0版本的安装文件，请运行之。
 (准备提供自动识别和手动填验证码两种方式供选择)
 * Chrome浏览器需要Chrome driver。在Chrome网址栏中输入Chrome://version查看版本，在
 [Chrome Driver下载地址](http://chromedriver.storage.googleapis.com/index.html)下载对应版本（最接近）的Driver，
并将其路径加入系统变量Path。（Selenium默认支持Firefox，IE/Edge/Chrome需安装对应driver）

 
 ### 功能介绍
 * 获取教学信息服务网(i.sjtu.edu.cn)和课表查询网(kbcx.sjtu.edu.cn)信息
 * 一键连接Zoom网课会议室
 
 
 
 #### 联系作者
 肖 鹏宇  (pydxflwb@sjtu.edu.cn)
 
 本文档最近更新日期: Mar 29 2020
 