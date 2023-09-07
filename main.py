# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import os
import sys
import time

from utils.config import writeConfig, readConfig
from utils.logutils import LogUtils

logger = LogUtils()


def welcome():
    os.system('cls')
    print("""
    *****************************************************************************   
    *         __  __ _____ _____  ______ _____     _____ _ _            _       *
    *    |  \/  |_   _|  __ \|  ____|  __ \   / ____| (_)          | |          *
    *    | \  / | | | | |  | | |__  | |__) | | |    | |_  ___ _ __ | |_         *
    *    | |\/| | | | | |  | |  __| |  ___/  | |    | | |/ _ \ '_ \| __|        *
    *    | |  | |_| |_| |__| | |____| |      | |____| | |  __/ | | | |_         *
    *    |_|  |_|_____|_____/|______|_|       \_____|_|_|\___|_| |_|\__|        *                                                    
    *****************************************************************************  
    *                               Project URL: https://github.com/hz157/MIDEP *
    *                                                   Client Date: 2023-02-03 *
    *****************************************************************************                                
    """)
    print(f"Welcome MIDEP Client, Start Time: {str(datetime.datetime.now())}")
    if readConfig('config', 'server_addr') is None:
        print("首次启动，请设置服务器地址")
        setServer()
    else:
        print(f"Server addr: {readConfig('config', 'server_addr')}")


def setServer():
    os.system('cls')
    print("输入服务器地址：（如：api.xxx.com），默认HTTPS")
    addr = input()
    if writeConfig('config', 'server_addr', addr):
        print("保存成功")
        time.sleep(3)
        os.system('cls')
        menu()


def createTask():
    os.system('cls')
    print("输入任务所需关键字")
    keyword = input()
    print("输入任务优先级 (0 > 1 > 2 > 3 > 4 > 5")
    priority = input()
    print("截止时间 (2023-01-01 00:00:00)")
    deadline = input()
    print(keyword, priority, deadline)


def readKeywordData():
    os.system('cls')
    print("输入任务所需关键字")
    keyword = input()
    print("""
    1.  TXT保存（Default）
    2.  CSV保存
    """)


def menu():
    print("""
             Menu （请输入选项前的序号并回车）
    1.  设置服务器地址
    2.  创建任务
    3.  读取关键字数据
    4.  更新Cookie
    q.  退出
    """)
    listenKey = input()
    try:
        if listenKey == 'q' or listenKey == 'Q':
            exit()
        if eval(listenKey) == 1:
            setServer()
        elif eval(listenKey) == 2:
            setServer()
        elif eval(listenKey) == 3:
            setServer()
        elif eval(listenKey) == 4:
            setServer()
    except Exception as e:
        logger.error(e)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    welcome()
    while True:
        menu()
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
