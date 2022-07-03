# adjacency flow

用于描述空间/时间上近邻的流的工具

## 什么是空间近邻效应？

> **空间近邻效应**就是指区域内各种经济活动之间或各区域之间的空间位置关系对其相互联系所产生的影响。

现在以人口预测模型为例

在空间邻近的模型下加入了时间相关矩阵，使得人口预测模型更加合理

> 一个空间邻接矩阵表（地区间的相邻）/ 包含转换后的json格式
>
> 一个流量表（地区间的流量）

## 界面

![image-20220610114418293](img/image-20220610114418293.png)

## 编译
> -F	显示命令行
>
> -i	图标
>
> --upx-dir	[UPX压缩](https://github.com/upx/upx/releases/tag/v3.96)

pyinstaller --clean -F -i  .\favicon.ico .\网络相邻.py --upx-dir=D:\env\upx-3.96-win64\upx.exe

![image-20220114104654683](img/image-20220114104654683.png)

