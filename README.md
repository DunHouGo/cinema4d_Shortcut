# Shortcut
Custom class to manipulate Shortcuts in Cinema 4D.

感谢@ferdinand

如何在Cinema 4D中查找和删除快捷方式。

在C4D内部,快捷键通过shortcut sequence绑定,通过input events侦测.

keySequence: 键盘输入序列, e.g., [c4d.QUALIFIER_SHIFT, '1'].

keySequence : e.g.

    [c4d.QUALIFIER_SHIFT, c4d.QUALIFIER_ALT, "S", "T"]

对应快捷键为 SHIFT + ALT + S ~ T.

strokeData (list): 由修饰键+Key组成的元组列表

    strokeData: list[tuple[int, int]]

### 换算
```text
内部运算逻辑为:
    1.所有修饰键 或 在一起 (ORed) or sum
    2.支持多重连续按键 , 比如 M~S
所以 SHIFT + ALT + S ~ T 的实际数值对应为 
    [1, 4, "S", "T"]
换算为
    [(5,83),(84)]
运算为    
[  (5, 83),      (qualifier = 1 | 4 = 5, key = ASCII_VALUE("S"))
    (84)         (qualifier = 0        , key = ASCII_VALUE("T") ]
```

Shortcut bc (c4d.BaseContainer): 快捷键容器结构.
```text
   Container Access             ID     Description
   bc[0]                          0    第一个key stroke(修饰键序列).
   bc[1]                          1    第一个key stroke(ASCII键值).
   bc[10]                        10    key stroke(修饰键序列)(可选).
   bc[11]                        11    第一个key stroke(ASCII键值)(可选).
   [...]
   bc[990]                      990    最大[99]key stroke(修饰键序列)(可选).
   bc[991]                      991    最大[99]key stroke(ASCII键值)(可选).

   bc[c4d.SHORTCUT_PLUGINID]   1000    插件ID.
   bc[c4d.SHORTCUT_ADDRESS]    1001    指定语境(生效管理器).
   bc[c4d.SHORTCUT_OPTIONMODE] 1002    是否打开选项.
```
对于多重快捷键,e.g., M ~ S, 每个index都乘10, 也就是范围[0,990], 共99个.

```text
示例一:
    按键为 "0" .
        1."0"的ASCII编码为48.
        2.没有修饰键

        #   0: 0
        #   1: 48
        #   1000: 200000084 # pID
        #   1001: 0
        #   1002: 0    
```

### Windows ID
目前没有地方能查询到（包括symbol.h文件）, 我找到的获取途径是通过FindShortcutAssign，指认到管理器后查询。这里罗列出一些常用ID:
```python
ARNOLD_IPR: int = 1032195
ARNOLD_SHADER_NETWORK: int = 1033989
ASSET_BROWSER: int = 1054225
ATTRIBUTTE_MANAGER: int = 1000468
CONSOLE: int = 10214
CORONA_NODE_MANAGER: int = 1040908
LAYER_MANAGER: int = 100004704
MATERIAL_MANAGER: int = 150041
NODEEDITOR_MANAGER: int = 465002211
OBJECT_MANAGER: int = 100004709
PICTURE_VIEWER: int = 430000700
PROJECT_ASSET_INSPECTOR : int = 1029486
TIMELINE_MANAGER: int = 465001516
XPPRESSO_MANAGER: int = 1001148
TAKE_MANAGER: int = 431000053
RENDER_QUEUE: int = 465003500
RENDER_SETTING: int = 12161
VIEWPORT: int = 59000
```
