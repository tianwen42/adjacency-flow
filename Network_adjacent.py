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

spacialflow=pd.read_excel(r'{}'.format(spacialMatrix))



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
            flow=flow.fillna(value=0)
            CreatSpatialDict(spacialflow)
            text1.insert('insert', "sp_dict建立成功\n")
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
    else:
        text1.insert('insert','至少输入一个文件\n')



def CreatSpatialDict(spacialflow):
    citys=spacialflow.columns
    global sp_dict
    sp_dict={}
    for row in spacialflow.itertuples():
        stocks_list=list(row)
        ad_index=[x-1 for x in range(len(stocks_list)) if stocks_list[x]==1]
        sp_dict[row[0]]=list(citys[ad_index])
    print('sp_dict建立成功')
    

def getAdjacentFlow(origin, destination):
    Adlist=[]
    sameOri=flow[flow['转出地'].str.contains(origin)]
    sameDes=flow[flow['转入地'].str.contains(destination)]
    Adlist1=sameOri[sameOri['转入地'].isin(sp_dict[destination])].ID.tolist()
    Adlist2=sameDes[sameDes['转出地'].isin(sp_dict[origin])].ID.tolist()
    Adlist=Adlist1+Adlist2
    return Adlist


readSpacialMatrix(spacialMatrix)
def start():
    global flow
    global W_OR
    
    W_OR = pd.DataFrame(index=(i for i in range(1, flow.shape[0] + 1)),
                        columns=([i for i in range(1, flow.shape[0] + 1)]))
    for row in flow.itertuples():
        try:
            netAdjacentList=getAdjacentFlow(row.转出地, row.转入地)
            print(row.ID, netAdjacentList)
            W_OR.loc[row.ID,netAdjacentList]=1
        except Exception as ex:
            print('ID={}出错'.format(row.ID))
            print('发生错误{}'.format(ex))
    print('正在保存')
    W_OR.dropna(axis=0,how='all').dropna(axis=1,how='all').fillna(value=0).to_excel('{}-resualt.xlsx'.format(flowData[:flowData.find('.')]))


bt1 = tk.Button(window, text='选择流文件', width=15, height=2, command=open_file)
bt1.pack()
bt2 = tk.Button(window, text='确定', width=15, height=2, command=confrim)
bt2.pack()

window.mainloop()  # 显示