# !/user/bin/env Python3
# -*- coding:utf-8 -*-

# 计算网络邻接矩阵

import tkinter as tk
from tkinter import filedialog, dialog
import os
import pandas as pd


window = tk.Tk()
window.title('计算网络邻接')  # 标题
window.geometry('500x500')  # 窗口尺寸

file_path = ''

file_text = ''

text1 = tk.Text(window, width=50, height=10, bg='grey', font=('Arial', 12))
text1.pack()


spacialMatrix='空间矩阵.xlsx'#
flowData=''
timeFlowData=''



def readSpacialMatrix(spacialMatrixName):
    global adjacent_table
    try:
        adjacent_table = pd.read_excel(r'{}'.format(spacialMatrixName))
        file_text = '空间矩阵shape：{0}*{1}\n'.format(adjacent_table.shape[0],adjacent_table.shape[1])
        text1.insert('insert', file_text)
    except:
        text1.insert('insert', "请检查当前路径含有'空间矩阵.xlsx'\n")


def open_file():
    '''
    打开文件
    :return:
    '''
    global flowData
    global flow
    global file_text
    if(os.path.exists(spacialMatrix)):
        flowData = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(os.getcwd())))
        print('打开流文件：', flowData)
        try:
            flow = pd.read_excel(r'{}'.format(flowData))
        except:
            print('请选择空间矩阵文件')
            return
        if flowData is not None:
            file_text = '流文件shape：{0}*{1}'.format(flow.shape[0], flow.shape[1])
            text1.insert('insert', file_text)
    else:
        text1.insert('insert', "请检查当前路径含有'空间矩阵.xlsx'\n")



def confrim():
    global file_path
    global file_text
    
    file_text = text1.get('1.0', tk.END)
    if(flowData!=''):
        start()
        print('保存完成:'+'{}_resualt.xlsx'.format(flowData[:flowData.find('.')]))
        print('保存文件：', file_path)
    else:
        text1.insert('insert','至少输入一个文件\n')





def get_AdjacentFlow(origin,destination):
    ID=flow[flow['转出地'].str.contains(origin) & flow['转入地'].str.contains(destination)]['ID']
    destinationFlow=adjacent_table.loc[adjacent_table.index.str.contains(destination)]
    if(destinationFlow.empty):
        print('it is empty')
    else:
        spacialDes=destinationFlow.T.dropna().T
        netAdjacent1=flow[flow['转出地'].str.contains(origin) & flow['转入地'].isin(spacialDes.columns.tolist())]
        originFlow=adjacent_table.loc[adjacent_table.index.str.contains(origin)]
        adjacentOri=destinationFlow.T.dropna().T
        spacialOri=adjacent_table.loc[adjacent_table.index.str.contains(origin)].T.dropna().T
        netAdjacent2=flow[flow['转出地'].isin(spacialOri.columns.tolist()) & flow['转入地'].str.contains(destination)]
        netAdjacentList=pd.concat([netAdjacent1,netAdjacent2],axis=0,join='inner')['ID'].tolist()
        print(netAdjacentList)
        for j in netAdjacentList:
            W_OR.loc[ID,j]=1


def timeAdjacentFlow(origin,destination):
    ID=flow[flow['转出地'].str.contains(origin) & flow['转入地'].str.contains(destination)]['ID']
    destinationFlow=adjacent_table.loc[adjacent_table.index.str.contains(destination)]
    if(destinationFlow.empty):
        print('it is empty')
    else:
        pass

readSpacialMatrix(spacialMatrix)
def start():
    global flow
    global W_OR
    
    W_OR = pd.DataFrame(index=(i for i in range(1, flow.shape[0] + 1)),
                        columns=([i for i in range(1, flow.shape[0] + 1)]))
    for index, row in flow.iterrows():
        try:
            get_AdjacentFlow(row.转出地,row.转入地)
            continue
        except:
            print('出错了')
            print(row)
    W_OR.dropna(axis=0,how='all').dropna(axis=1,how='all').fillna(value=0).to_excel('{}-resualt.xlsx'.format(flowData[:flowData.find('.')]))


bt1 = tk.Button(window, text='选择流文件', width=15, height=2, command=open_file)
bt1.pack()
bt2 = tk.Button(window, text='确定', width=15, height=2, command=confrim)
bt2.pack()

window.mainloop()  # 显示