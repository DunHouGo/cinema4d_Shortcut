# Shortcut
### Custom class to manipulate Shortcuts in Cinema 4D.

Last Update : 2022/12/01

Author: 王敦厚Go (DunHou)

Written for Maxon Cinema 4D R2023.1.0 Python version 3.9.1

Custom Cinema 4D Shortcut Functions

# Intro
如何在Cinema 4D中查找和删除快捷方式。

# Funtions :
1.获取插件快捷键列表 
2.获取快捷键序号(序号,不存在时返回False) 
3.删除快捷键 4.获取快捷键指认的插件id和管理器id 
5.添加快捷键到对应的插件id和管理器id(可选) 
6.KeySequence转换StrokeData 
7.检测快捷键是否已经绑定给指定插件 
8.为插件添加快捷键(监测快捷键指认)

# Example :
如何在插件中使用（基础示例）