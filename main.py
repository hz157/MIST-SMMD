# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: dev
# @FileName: main
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 4/2/2023 下午3:43

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import os

from Config import config
from Network.Sina import getArticlePagesByKeyword, getArticlePageInfo
from Utils.logutils import LogUtils

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
    *       Tips:   Turning on the proxy may generate an inaccessible Weibo URL *
    *                               Project URL: https://github.com/hz157/MIDEP *
    *                                                   Client Date: 2023-02-03 *
    *****************************************************************************                                
    """)
    print(f"Welcome MIDEP Client, Start Time: {str(datetime.datetime.now())}")
    testCookie()


def displayMenu():
    os.system('cls')
    menu()


def anykey():
    print('按任意键继续')
    input()


def createTask():
    print("输入任务所需关键字")
    keyword = input()
    print("输入任务优先级 (0 > 1 > 2 > 3 > 4 > 5")
    priority = input()
    print("截止时间 (2023-01-01 00:00:00)")
    deadline = input()
    anykey()
    displayMenu()


def setDatabase():
    param = {
        'host': '127.0.0.1',
        'port': '3306',
        'username': None,
        'password': None,
        'database': None,
    }
    try:
        print("输入数据库地址  （Default: 127.0.0.1）")
        param['host'] = input()
        if param['host'] == '' or param['host'] is None:
            param['host'] = '127.0.0.1'
        print("输入数据库端口  （Default: 3306）")
        param['port'] = input()
        if param['port'] == '' or param['port'] is None:
            param['port'] = '3306'
        print("输入数据库用户名")
        param['username'] = input()
        print("输入数据库密码")
        param['password'] = input()
        print("输入数据库名称")
        param['database'] = input()
        for i in param:
            config.writeConfig('mysql', i, param[i])
        print("SetDatabase Success")
    except Exception as e:
        logger.error(e)
        print("SetDatabase Error")
    anykey()
    displayMenu()


def setCookie():
    print("""
            SetCookie
    1.  桌面端 Cookie   （s.weibo.cn）
    2.  移动端 Cookie   （m.weibo.com）
    q.  返回菜单
    """)
    listenKey = input()
    try:
        if listenKey == 'q' or listenKey == 'Q':
            displayMenu()
        if int(listenKey) == 1:
            os.system('cls')
            print("请粘贴桌面端 Cookie")
            config.writeConfig('cookie', 'pc', input())
            testCookie('pc')
        elif int(listenKey) == 2:
            os.system('cls')
            print("请粘贴移动端端 Cookie")
            config.writeConfig('cookie', 'mobile', input())
            testCookie('mobile')
        print("SetCookie Success")
    except Exception as e:
        logger.error(e)
        print("SetCookie Error")
    anykey()
    displayMenu()


def testCookie(type: str = 'all'):
    print("正在测试Cookie有效性")
    if type == 'pc' or type == 'all':
        pages = getArticlePagesByKeyword('上海')
        print(pages)
        if pages != 1:
            print('     桌面端 Cookie 有效')
        else:
            print('     桌面端 Cookie 无效，请更新')
    if type == 'mobile' or type == 'all':
        pageInfo = getArticlePageInfo('4756167840760485')
        print(pageInfo)
        if pageInfo is not None:
            print('     移动端 Cookie 有效')
        else:
            print('     移动端 Cookie 无效，请更新')
    anykey()
    displayMenu()


def readKeywordData():
    print("输入任务关键字")
    keyword = input()
    print("""
            File Format 文件格式
    1.  TXT保存（Default）
    2.  CSV保存
    q.  返回菜单
    """)
    anykey()
    displayMenu()


def setParam():
    print("""
            SetParam （请输入选项前的序号并回车）
    1.  更新/设置 Cookie
    2.  测试 Cookie
    3.  更新/设置 Database
    4.  更新/设置 File Save Path
    5.  格式化本地配置
    q.  返回菜单
    """)
    listenKey = input()
    try:
        if listenKey == 'q' or listenKey == 'Q':
            displayMenu()
        if int(listenKey) == 1:
            os.system('cls')
            setCookie()
        elif int(listenKey) == 2:
            os.system('cls')
            testCookie()
        elif int(listenKey) == 3:
            os.system('cls')
            setDatabase()
        elif int(listenKey) == 4:
            os.system('cls')
            setDatabase()
    except Exception as e:
        logger.error(e)


def menu():
    print("""
             Menu （请输入选项前的序号并回车）
    1.  创建任务
    2.  读取关键字数据
    3.  参数设置
    4.  测试Cookie
    q.  退出
    """)
    listenKey = input()
    try:
        if listenKey == 'q' or listenKey == 'Q':
            exit()
        if int(listenKey) == 1:
            os.system('cls')
            createTask()
        elif int(listenKey) == 2:
            os.system('cls')
            readKeywordData()
        elif int(listenKey) == 3:
            os.system('cls')
            setParam()
        elif int(listenKey) == 4:
            os.system('cls')
            testCookie()
    except Exception as e:
        logger.error(e)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    welcome()
    while True:
        menu()
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
