# -*- coding: utf-8 -*-
from genericpath import exists
import io
from operator import index
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

import re
import os
import datetime

# 获取当前系统时间
sysNow = datetime.datetime.now()

# 目标文件夹名称
dirName = "files"
# 写入文件夹名称
wDirName = "urlFiles"
# 目标文件夹路径
dirPath = ".\\"+dirName
# 日志文件名称
logFileName = "info_"+str(sysNow.year)+str(sysNow.month)+str(sysNow.day)+str(sysNow.hour)+str(sysNow.minute)+str(sysNow.second)
# 日志文件保存路径
logFilePath = ".\\Log"
# 批处理文件保存位置
batPath = '.\\download.bat'

# 判断日志文件夹是否存在，不存在就创建
if not os.path.exists(logFilePath):
    os.makedirs(logFilePath)

# (函数)用于打印日志文件
def printLog(msg):
    print(msg)
    log = open(logFilePath+"\\"+logFileName+".log","a")
    log.write(msg+"\n")
    log.close()

# (函数)用于设置用于下载的批处理文件(不建议修改此函数的内容)
def setDownloadBat(type,fPath):
    batStr = ''
    if type==0:
        if exists(batPath):
            os.remove(batPath)
        batStr = '@echo off\n'
    elif type==1:
        batStr += r'attrib -h -s -r -a %0'+'\ndel %0\npause'
    elif type==2:
        downloadDirPath = ".\\download\\"+fPath.split('\\')[2]
        fPath = r'%cd%'+fPath.split('.')[1]+'.'+fPath.split('.')[2]
        batStr += r'for /f "delims=," %%i in ('+fPath+r') do ('+"\n"+r'package'+"\\"+'you-get -o %cd%\download'+"\\"+fPath.split('\\')[2]+r'\ %%i'+"\n)\n"
        if not exists(downloadDirPath):
            os.makedirs(downloadDirPath)
    bat = open(batPath,"a")
    print(batStr)
    bat.write(batStr)
    bat.close()

# 判断要读取的文件夹是否存在，不存在将自动创建
if not os.path.exists(dirPath):
    os.makedirs(dirPath)
    printLog("请先将需要抓取url的文件复制到文件夹["+dirName+"]中！")
    sys.exit(0)
else:
    printLog("已检测到文件夹["+dirName+"]...")

# 按路径读取出文件夹中的所有文件名称，类型为集合
files = os.listdir(dirPath)

# 判断目标文件夹中是否有文件
if len(files)==0:
    printLog("没有在文件夹["+dirName+"]中读取到文件！")
    sys.exit(0)
else:
    printLog("已读取到文件夹["+dirName+"]中的文件:")

# 初始化批处理文件
setDownloadBat(0,'')
os.system("attrib +a +s +h "+batPath)

for f in files:
    printLog(f)

# 循环文件名称集合
for file in files:
    printLog('\n开始检索文件('+file+')下的URL：')
    fileName = file.split('.')[0]
    # 拼接要读取的文件路径
    filePath = dirPath+"\\"+file
    # 拼接创建文件夹路径
    wDirPath = ".\\"+wDirName+"\\"+fileName
    # 拼接要写入的文件路径
    wFilePath = wDirPath+"\\"+fileName+".txt"
    
    setDownloadBat(2,wFilePath)

    printLog("正在准备创建文件夹["+fileName+"]...")

    # 判断文件夹是否存在，不存在就创建
    if not os.path.exists(wDirPath):
        printLog("开始创建文件夹["+fileName+"]...")
        os.makedirs(wDirPath)
        printLog("文件夹["+fileName+"]创建成功！")
    else:
        printLog("文件夹["+fileName+"]已存在！")

    printLog("准备将url写入到文件("+fileName+".txt)中...")

    # 按文件路径打开文件
    with open(filePath, encoding='utf-8') as fileContent:
        printLog("开始将url写入到文件("+fileName+".txt)中...")

        # 记录写入文件的次数
        i = 1
        # 循环文件内容每一行
        for line in fileContent:
            # 用正则匹配文件内容中的url
            urls = re.findall('https?://.+\.jpg', line)
            urls += re.findall('https?://.+\.jpeg', line)
            urls += re.findall('https?://.+\.png', line)
            urls += re.findall('https?://.+\.gif', line)
            urls += re.findall('https?://.+\.webp', line)
            urls += re.findall('https?://.+\.ico', line)
            urls += re.findall('https?://.+\.svg', line)
            for url in urls:
                # print(url)
                # 打开将写入的文件
                w = open(wFilePath,"a")
                wUrl = ''
                # 如果是第一次写入文件，就不在内容前面加','也不换行
                if i == 1:
                    wUrl = url
                else:
                    wUrl = ",\n"+url
                # 写入内容
                w.write(wUrl)
                # 关闭文件
                w.close()
                i = i+1

        printLog("文件("+fileName+".txt)已写入完成！")
printLog("\n已成功将所有文件写入到文件夹["+wDirName+"]中")
setDownloadBat(1,'')
os.system(batPath)