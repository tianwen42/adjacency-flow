# !/user/bin/env Python3
# -*- coding:utf-8 -*-

# 计算网络邻接矩阵

import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import pandas as pd

window = tk.Tk()
window.title('计算网络邻接')  # 标题
window.geometry('500x500')  # 窗口尺寸

text1 = tk.Text(window, width=50, height=10, bg='grey', font=('Arial', 12))
text1.pack()

spacialMatrix = ''  # 空间邻接矩阵
flowMatrix = ''
timeFlowData = ''


def readSpacialMatrix(spacialMatrixName: str):
    isSuccessful = False
    try:
        outMatrix = pd.read_excel(r'{}'.format(spacialMatrixName))  # 读空间矩阵
        isSuccessful = True
    except:
        messagebox.showinfo('有点问题', "请检查当前路径含有'空间矩阵.xlsx'\n")
        text1.insert('insert', "请检查当前路径含有'空间矩阵.xlsx'\n")
    if isSuccessful:
        text1.insert('insert', '已检测到空间矩阵  shape：{0}*{1}\n'.format(outMatrix.shape[0], outMatrix.shape[1]))
    return outMatrix


def open_file():
    """
    打开文件
    return
    """
    flowDataFullName = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(os.getcwd())))
    if os.path.exists(flowDataFullName):
        try:
            flowData = pd.read_excel(r'{}'.format(flowDataFullName)).fillna(value=0)
            createSpatialDict(spacialMatrix)
            text1.insert('insert', "空间索引;建立成功\n")
        except:
            print('请选择空间矩阵文件')
            return
        if flowData is not None:
            text1.insert('insert', '流文件shape：{0}*{1}'.format(flowData.shape[0], flowData.shape[1]))
    else:
        text1.insert('insert', "请检查当前路径含有空间矩阵.xlsx'\n")


def createSpatialDict(spacialflow):
    citysName = spacialflow.columns
    global sp_dict
    sp_dict = {}
    for row in spacialflow.itertuples():
        stocks_list = list(row)
        ad_index = [x - 1 for x in range(len(stocks_list)) if stocks_list[x] == 1]
        sp_dict[row[0]] = list(citysName[ad_index])
        text1.insert('insert', '{}\n'.format(list(citysName[ad_index])))
    print('sp_dict建立成功')


def getAdjacentFlow(origin, destination):
    sameOri = flow[flow['转出地'].str.contains(origin)]
    sameDes = flow[flow['转入地'].str.contains(destination)]
    Adlist1 = sameOri[sameOri['转入地'].isin(sp_dict[destination])].ID.tolist()
    Adlist2 = sameDes[sameDes['转出地'].isin(sp_dict[origin])].ID.tolist()
    Adlist = Adlist1 + Adlist2
    return Adlist


spacialMatrix = readSpacialMatrix('空间矩阵.xlsx')


def calAdjacent():
    global flow
    W_OR = pd.DataFrame(index=(i for i in range(1, flow.shape[0] + 1)),
                        columns=([i for i in range(1, flow.shape[0] + 1)]))
    for row in flow.itertuples():
        try:
            netAdjacentList = getAdjacentFlow(row.转出地, row.转入地)
            print(row.ID, netAdjacentList)
            W_OR.loc[row.ID, netAdjacentList] = 1
        except Exception as ex:
            print('ID={}出错'.format(row.ID))
            print('发生错误{}'.format(ex))
    print('正在保存')
    W_OR.dropna(axis=0, how='all').dropna(axis=1, how='all').fillna(value=0).to_excel(
        '{}-result.xlsx'.format(flowMatrix[:flowMatrix.find('.')]))


def btn_confirm():
    text1.get('1.0', tk.END)
    if flowMatrix != '':
        calAdjacent()
        print('保存完成:' + '{}_result.xlsx'.format(flowMatrix[:flowMatrix.find('.')]))
    else:
        text1.insert('insert', '至少输入一个文件\n')


bt3 = tk.Button(window, text='选择空间邻接文件', width=15, height=2)
bt3.pack()

bt1 = tk.Button(window, text='选择流文件', width=15, height=2, command=open_file)
bt1.pack()

bt2 = tk.Button(window, text='确定', width=15, height=2, command=btn_confirm)
bt2.pack()

window.mainloop()  # 显示
