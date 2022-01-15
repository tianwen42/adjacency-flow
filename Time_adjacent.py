# !/user/bin/env Python3
# -*- coding:utf-8 -*-

# 计算时间邻接矩阵

import tkinter as tk
from tkinter import filedialog, dialog
import os
import pandas as pd
import numpy as np


window = tk.Tk()
window.title('计算时间近邻')  # 标题
window.geometry('500x500')  # 窗口尺寸

text1 = tk.Text(window, width=50, height=10, bg='grey', font=('Arial', 12))
text1.pack()


network_adjacentName = ''
timeflowDataName = ''


file_text = '需要输入网络的近邻文件&流的年份\n'
text1.insert('insert', file_text)


def open_file1():
    '''
    打开文件
    :return:
    '''
    global network_adjacentName
    global net_table
    network_adjacentName = filedialog.askopenfilename(
        title=u'选择文件', initialdir=(os.path.expanduser(os.getcwd())))
    print('打开网络近邻文件：', network_adjacentName)
    net_table = pd.read_excel(r'{}'.format(network_adjacentName))
    if network_adjacentName is not None:
        file_text = '网络近邻文件shape：{0}*{1}    '.format(
            net_table.shape[0], net_table.shape[1])
        text1.insert('insert', file_text)
        if(net_table.shape[0] == net_table.shape[1]):
            text1.insert('insert', '格式正确\n')


def open_file2():
    '''
    打开文件
    :return:
    '''
    global timeflowDataName
    global time_table
    timeflowDataName = filedialog.askopenfilename(
        title=u'选择文件', initialdir=(os.path.expanduser(os.getcwd())))
    print('打开流年份文件：', timeflowDataName)
    time_table = pd.read_excel(r'{}'.format(timeflowDataName))
    if timeflowDataName is not None:
        file_text = '流年份文件shape：{0}*{1}   '.format(
            time_table.shape[0], time_table.shape[1])
        text1.insert('insert', file_text)


def start():
    time_table.index = time_table['ID']
    years = time_table[['年份']].T
    net_adjancent = net_table.replace(0, np.nan)
    T_OR = net_table
    for index, row in net_adjancent.iterrows():
        try:
            idxList = row.dropna().T.index.tolist()
            for i in idxList:
                if int(years[index]) == int(years[i])-1:
                    print(index, i, 'yes')
                else:
                    print(index, i, 'no 置0')
                    T_OR.loc[index, i] = 0
            continue
        except:
            print('出错了')
    T_OR.replace(0, np.nan).dropna(axis=0, how='all').dropna(axis=1, how='all').fillna(
        value=0).to_excel('时间近邻结果.xlsx')


def confrim():
    file_text = text1.get('1.0', tk.END)
    print(network_adjacentName, timeflowDataName)
    if(network_adjacentName=='' or timeflowDataName==''):
        text1.insert('insert', '请输入两种文件\n')
    else:
        start()
        print('保存完成:\n'+"时间近邻结果.xlsx")


bt1 = tk.Button(window, text='选择网络近邻文件', width=15,
                height=2, command=open_file1)
bt1.pack()
bt3 = tk.Button(window, text='选择流的年份文件', width=15,
                height=2, command=open_file2)
bt3.pack()
bt2 = tk.Button(window, text='确定', width=15, height=2, command=confrim)
bt2.pack()

window.mainloop()  # 显示
