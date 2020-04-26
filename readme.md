# 一键网课助手

* [English Readme File](http://github.com/pydxflwb/KeyAssistant/tree/master/doc/readme_en.md)

_一键网课助手_ 是一个帮助SJTU学生快速登录Zoom平台含密码会议室的程序


 ## 最新更新
  
  * 2020.04.26：
  	
	第九周到来，目前程序发现的需要修改的几个bug：
		
	1.无法更新课表
	
	2.结课的课程不会消失
	
	3.多线程需求强烈
	
	我会尽快做出修改
	

 ## 运行环境及库依赖
 （目前仅适用于Windows 10系统，使用Mac的同学实在抱歉）
 * Python 3.5, 3.6, 3.7（推荐3.6.x）稳定可用，其余版本不保证可用性
 * selenium
 * requests	 
 * PyQt5
 * baidu-aip (百度提供的OCR接口)
 * Pywin32
 * pyautogui
 * pyHook(Python 3版本可能需要.whl，已提供)
 * pyUserInput(要求安装Pywin32和pyHook)
 
 ## 安装
 * pip install -r requirements.txt / conda install -r requirements.txt
 * Chrome浏览器需要Chrome driver。在Chrome网址栏中输入[Chrome://version](Chrome://version)查看版本，在
 [Chrome Driver下载地址](http://chromedriver.storage.googleapis.com/index.html)下载对应版本（版本号__小于等于__你的Chrome版本且最接近）的Driver，__放在Python安装路径文件夹内（如 /Program Files(x86)/Python36/ 路径下）和Chrome.exe的文件夹下__，把Chrome的文件夹路径加入系统变量Path。（Selenium默认支持Firefox，Chrome需安装对应driver）
 * 对于部分库(pyHook)，Python3 pip可能无法安装，请下载使用[whl文件](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyHook)安装（或者使用conda安装）（现在pyHook文件夹为大家提供了1.5.1版本x64的安装包，请自行选用）
 
 ## 功能介绍
 
 ### 再也不怕早起手忙脚乱！不需要到处找房间号和密码！
 * 一键登录当前时间对应的课程Zoom会议室！
 * 可以自己设置每门课对应的时间，在时间段内点击一键上课都是这节课哦！
  
 ## 使用说明
 ### 大体使用说明
 * 主程序：MainWindow.py
 * 一键程序：OneKey.py 
 * 启动前：安装环境后，将/src/GUI中的两个.bat文件建立快捷方式拖到桌面即可方便地启动
 * 第一次使用，打开主程序，在左边输入框中输入自己的jaccount账户密码，选择浏览器（目前支持Chrome/Firefox）。程序会打开浏览器，
 模拟登陆获取并存储课程信息。
 
 * 调整自己的预设时间：通过双击列表课程来显示课程的详细信息，在下面的时间修改框来修改预设时间。
 * __预设时间是什么？__ :预设时间是一键上课的参数，当前时间打开一键上课就是这个时间段内对应的课程。例如:我设置操作系统在7:45
 --9:40，在这个时间段内打开一键上课程序，都会是操作系统课程！我给大家预设的时间是开始前15分钟--课程结束，因此你也可以不改预设时间哦。
 * __老师提早下课，我想先登陆别的课！__ :主程序--双击选择你想进入的课程--右下角进入课程按钮，就直接进去啦！
 
 
 ### 你可能提出的问题
 * __一键登录的课程会刷新吗？__:会的。我设置每30s刷新一次。因此，如果下一节课设置的起始时间是9:50，你不巧地在9:49:50启动了程序，那么程序会在9:50:20刷新到下一节课。只需要等待30秒！
 * __本人不对因此造成的迟到负任何责任__：想来不用这个程序你也照样会迟到。还有，早点起来上课。
 * __为什么程序和Zoom无响应？__:无响应不是因为出了问题，而是我设置了不成功则继续请求，一般会出现在网络不好或者已经打开会议室时。超时之后会弹出提示框。请您根据提示框检查问题。如果不能解决请提issues或联络我。
 * __界面好简陋啊__: 我懒。
 
 ### 这个程序不能做到的事
 * __可以自动连续上课吗？__:对不起，暂时我还没有写这部分的自动模块QwQ，所以下一节课你还需要手动点击几下。（但是只要两步！打开一键程序，点击一键上课。）
 * __能替我签到回答问题吗？__:学习是自己的事，同学。这个程序只是帮你省去找会议号和密码登录的麻烦
 * __Edge浏览器不能用吗？__:对不起，我暂时没加，其实也很容易，如果你们提这方面issues，我会考虑加的。（Selenium对应的浏览器driver需要自行下载安装）
 
 ### 如果您想对本程序进行后续开发
 * __为什么有些部分代码那么臃肿？__:对不起，我花的时间并不多，代码显得很粗糙。也许我或者您可以对代码进行新的重构？

 * __有些地方有bug！__:欢迎issues，欢迎pull requests，欢迎建议和意见。
  
  
 
 ## 更新说明
 
 * 2020.04.08:  这个程序的一期功能代码已经上传！
 * 2020.04.09:  __现在你可以使用基本的一键网课助手了！__
            
            当前版本提供基本使用功能
            因为库很多，经过打包后程序文件很大（200MB），运行速度也受较大影响，因此Github上不提供exe文件
            烦请大家使用Python解释器运行程序，或者使用.bat文件，均在/src/GUI中，可以创建快捷方式放到桌面            
 * __[ 重要说明 ]__ 2020.04.10 : __经过一些测试，解答一些配置过程中出现的问题__
            
   1.使用conda虚拟环境安装库和使用时，使用.bat运行的方法：编辑/src/GUI下的两个.bat文件，在两行代码中间插入
  
              call activate 你运行本程序的虚拟环境名称
    该方法需要conda加入环境变量
            
   2.关于chromedriver不在路径中：如果填写学号和密码连接SJTU总是提示超时，请检查chromedriver
      
      * 是否下载的是对应自己Chrome版本的chromedriver，并把chromedriver.exe所处文件夹的路径添加到了环境变量
      * Python环境放在Python文件夹下，conda则放在conda文件夹下
      * 如果还不能使用，请[修改代码](https://github.com/pydxflwb/KeyAssistant/blob/261a81c0b417f124d68a51a0bb6af3d3213fe0d9/src/GUI/MainWindow.py#L81)
                修改webdriver.Chrome(executable_path='你的chromedriver所在路径')
      * 直接提出issues或者联络我。若您有兴趣，也可对InfoRequestWidget.py源码部分的try-except相关代码修改掉，进行debug
                
   3.关于无响应和超时等待的一点说明
    
                        我暂时没有使用QThread进行多线程处理，以防止等待时无响应
                        但无响应时程序没有发生问题，它只是在反复等待和请求，在cmd中你可以看见打印出来的等待轮次
                        所以请耐心等待连接，或者直接关闭程序，检查Zoom状况后再运行

 * 2020.04.19：近期可能的更新预告
	
	1.一键按钮增加了一只可爱的初音fufu！开发完成后续一并上线 
	
	2.关于jaccount密码输入时的保密选项问题
	
	3.使用QThread线程继续优化用户交互的问题
  
 * 2020.04.20： 
	
	1.可爱fufu来了！
	[点我看fufu](https://github.com/pydxflwb/KeyAssistant/tree/master/github_gif/fufu.gif)
	
	2.jaccount密码保密设置已经更新！
  
  * 2020.04.26：
  	
	第九周到来，目前程序发现的需要修改的几个bug：
		
	1.无法更新课表
	
	2.结课的课程不会消失
	
	3.多线程需求强烈
	
	我会尽快做出修改
  
 ## 联系作者
 肖 鹏宇  (pydxflwb@sjtu.edu.cn)
 欢迎提交issue! 欢迎使用和改进！


 ### 致谢
   * KunYao Lan（test）
   * Xin Yuan（test and debug）
   
  
 本文档最近更新日期: April 26 2020
 
 License: MIT License
