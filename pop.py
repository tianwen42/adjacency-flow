#-- coding:utf8 --
import tkinter
tk = tkinter.Tk()
#设置窗口标题
tk.title("BMI计算器")
#设置窗口代销
tk.geometry("400x400")

Bmi1 = tkinter.StringVar()
Bmi2 = tkinter.StringVar()
#添加Label和Entry
#1、设置升高标签和输入框
#1-1身高标签
label_height = tkinter.Label(tk,text = "身高",font = ("隶书",20))
label_height.place(x = 10,y = 10,width = 80,height = 40)

#1-2身高输入框
entry_height = tkinter.Entry(tk,textvariable = tkinter.StringVar(),
font = ("隶书",20))
entry_height.place(x = 90,y = 10,width = 80,height = 40)

#1-3身高单位
label_cm = tkinter.Label(tk,text = "cm",font = ("隶书",20))
label_cm.place(x = 170,y = 10,width = 40,height = 40)

#2、设置体重标签和输入框
#2-1体重标签
label_weight = tkinter.Label(tk,text = "体重",font = ("隶书",20))
label_weight.place(x = 10,y = 60,width = 80,height = 40)

#2-2体重输入框
entry_weight = tkinter.Entry(tk,textvariable = tkinter.StringVar(),
font = ("隶书",20))
entry_weight.place(x = 90,y = 60,width = 80,height = 40)
#2-3体重单位kg
label_kg = tkinter.Label(tk,text = "kg",font = ("隶书",20))
label_kg.place(x = 170,y = 60,width = 40,height = 40)
#添加计算按钮Button
def bmi():
   bmi_set = round(float(entry_weight.get())/
   (float(entry_height.get())*float(entry_height.get()))*10000,2)
   if bmi_set < 18.5:
      result = ("您的BMI为：",bmi_set)
      abc = ("过轻")
   elif 18.5 <= bmi_set <= 25:
      result = ("您的BMI为：",bmi_set)
      abc = ("正常")
   elif 25 <= bmi_set <= 28:
      result = ("您的BMI为：",bmi_set)
      abc = ("过重")
   elif 28 <= bmi_set <= 32:
      result = ("您的BMI为：",bmi_set)
      abc = ("肥胖")
   else:
      result = ("您的BMI为：",bmi_set)
      abc = ("严重肥胖")
   Bmi1.set(result)
   Bmi2.set(abc)

button_bmi = tkinter.Button(tk,text = "BMI",font = ("隶书",20),
command = bmi)
button_bmi.place(x = 50,y = 110,width = 300,height = 40)
#添加显示结果的输入框
entry_bmi1=tkinter.Entry(tk,textvariable = Bmi1,font=("隶书",20))
entry_bmi1.place(x = 30,y = 160,width = 340,height = 50)
entry_bmi2=tkinter.Entry(tk,textvariable = Bmi2,font=("隶书",20))
entry_bmi2.place(x = 30,y = 210,width = 340,height = 50)
tk.mainloop()