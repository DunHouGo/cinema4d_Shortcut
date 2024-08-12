import c4d
from dataclasses import dataclass,field
from typing import Optional, Union, TypeAlias
from pprint import pp

#=============================================
#                  Intro
#=============================================
"""
如何在Cinema 4D中查找和删除快捷方式。

在C4D内部,快捷键通过shortcut sequence绑定,通过input events侦测.


#! keySequence: 键盘输入序列, e.g., [c4d.QUALIFIER_SHIFT, '1'].

#keySequence : e.g.

    [c4d.QUALIFIER_SHIFT, c4d.QUALIFIER_ALT, "S", "T"]

对应快捷键为 SHIFT + ALT + S ~ T.

内部运算逻辑为:
    1.所有修饰键 或 在一起 (ORed) or sum
    2.支持多重连续按键 , 比如 M~S
所以 SHIFT + ALT + S ~ T 的实际数值对应为 
    [1, 4, "S", "T"]
换算为
    [(5,83),(84)]
运算为    
[  (5, 83),     # (qualifier = 1 | 4 = 5, key = ASCII_VALUE("S"))
    (84)        # (qualifier = 0        , key = ASCII_VALUE("T") ]
    
ord(): str => ASCII


#! Shortcut bc (c4d.BaseContainer): 快捷键容器结构.

#   Container Access             ID     Description
#   bc[0]                          0    第一个key stroke(修饰键序列).
#   bc[1]                          1    第一个key stroke(ASCII键值).

#   bc[10]                        10    key stroke(修饰键序列)(可选).
#   bc[11]                        11    第一个key stroke(ASCII键值)(可选).
#   [...]
#   bc[990]                      990    最大[99]key stroke(修饰键序列)(可选).
#   bc[991]                      991    最大[99]key stroke(ASCII键值)(可选).

#   bc[c4d.SHORTCUT_PLUGINID]   1000    插件ID.
#   bc[c4d.SHORTCUT_ADDRESS]    1001    指定语境(生效管理器).
#   bc[c4d.SHORTCUT_OPTIONMODE] 1002    是否打开选项.

对于多重快捷键,e.g., M ~ S, 每个index都乘10, 也就是范围[0,990], 共99个.

示例一:
    按键为 "0" .
        1."0"的ASCII编码为48.
        2.没有修饰键
        #   0: 0
        #   1: 48
        #   1000: 200000084 # pID
        #   1001: 0
        #   1002: 0    

示例二:
    按键为 "M~S" .
        1."M"的ASCII编码为77.
        2."S"的ASCII编码为83.
        3.没有修饰键
        #   0: 0
        #   1: 48
        #   1000: 200000084 # pID
        #   1001: 0
        #   1002: 0 

#! strokeData (list): 由修饰键+Key组成的元组列表

strokeData: list[tuple[int, int]]
"""

# Windows ID
# 目前没有地方能查询到（包括symbol.h文件）, 我找到的获取途径是通过FindShortcutAssign，指认到管理器后查询。
# 这里罗列出一些常用ID
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

#! keySequence:  list[typing.Union[int, str]]
#! 键盘输入序列列表, e.g., [c4d.QUALIFIER_SHIFT, '1'] , [4,'2'] , [0, 'Y']
#! strokeData (list): 由修饰键+Key组成的元组列表 [(5,83),(84)]

#=============================================
#                   Codes
#=============================================

# 这是快捷键在C4D中的数据结构,是由修饰键+Key组成的元组列表 如[(5,83),(84)]
@dataclass
class StrokeData:
    """This is the data structure of shortcut keys in C4D, it is a list of tuples consisting of modifier keys + Key. E.g[(5,83),(84)]"""
    data: list[tuple[int]] = field(default_factory=None)
        
    def __str__(self) -> str:
        return f"StrokeData: {self.data}, with shortcuts: {self.ToString()}"
            
    def ToString(self) -> str:
        """Generate a string representation of the StrokeData."""
        res = []
        separator = '~' 
        for item in self.data:
            index, shortcut = item
            shortkey = c4d.gui.Shortcut2String(index, shortcut)
            res.append(shortkey)            
        return separator.join(res)
    
    def IsValid(self) -> bool:
        """
        Check if the StrokeData is valid.

        Returns:
            bool: True if the StrokeData is valid, False otherwise.
        """
        if self.data is None:
            return False
        if not isinstance(self.data, list):
            False
        for item in self.data:
            if not isinstance(item, tuple):
                return False
        return True

    @property
    def Data(self) -> list[tuple[int]]:
        """The list data of the StrokeData."""
        return self.data

    @Data.setter
    def Data(self, value: list[tuple[int]]) -> None:
        self.data = value

# 这是用户可读的快捷键形式, 由修饰键+Key组成的列表, 如[c4d.QUALIFIER_SHIFT, '1']
@dataclass
class KeySequence:
    """This is the user-readable form of shortcuts, consisting of a list of modifier keys + Key, e.g.[c4d.QUALIFIER_SHIFT, '1']"""
    data: list[int, str] = field(default_factory=None)
            
    def CovertToStrokeData(self) -> StrokeData:
        """
        Convert KeySequence to StrokeData.

        ---
        Example:
        1.[c4d.QUALIFIER_SHIFT, '1'] => Output [(1, 49)]
        2.[c4d.QUALIFIER_SHIFT, c4d.QUALIFIER_ALT, "S", "T"] => Output [(5,83),(0,84)]

        Alt : c4d.QUALIFIER_ALT = 4
        
        Ctrl : c4d.QUALIFIER_CTRL = 2
        
        Shift : c4d.QUALIFIER_SHIFT = 1

        Returns:
            StrokeData: StrokeData of the KeySequence.
        """
        strokeData: list[tuple[int, int]] = []
        # A variable to OR together the qualifiers for the current key stroke.
        currentModifiers: int = 0
        # 获取 [strokeData]
        # 转换keySequence:[c4d.QUALIFIER_SHIFT, '1'] => Output [(1, 49)]
        for key in self.data:
            # Extend a modifier key sequence, e.g., SHIFT + ALT + CTRL
            if isinstance(key, (int, float)):
                currentModifiers |= key
            # A character key was found, append an input event.
            elif isinstance(key, str) and len(key) == 1:
                strokeData.append((currentModifiers, ord(key.upper())))
                currentModifiers = 0
            else:
                raise RuntimeError(f"Found illegal key symbol: {key}")
        return strokeData

    def ToString(self) -> str:
        """Generate a string representation of the StrokeData."""
        strokeData: StrokeData = self.CovertToStrokeData()
        return strokeData.ToString()

    def IsValid(self) -> bool:
        """
        Check if the KeySequence is valid.

        Returns:
            bool: True if the KeySequence is valid, False otherwise.
        """
        if self.data is None:
            return False
        for item in self.data:
            if not isinstance(item, (int, str)):
                return False
        return True

    @property
    def Data(self) -> list[tuple[int]]:
        """The list data of the KeySequence."""
        return self.data

    @Data.setter
    def Data(self, value: list[tuple[int]]) -> None:
        self.data = value

# We define a type alias for the data type of the shortcut.
KeyData = Union[KeySequence, StrokeData, list[int, str], list[tuple[int]]]

# Convert keys data to the StrokeData we need.
def ToStrokeData(data: KeyData) -> Optional[StrokeData]:
    """
    Convert given data to StrokeData.

    Args:
        data (Union[KeySequence, StrokeData, list[int, str], list[tuple[int]]]): the date we want to convert.

    Returns:
        Optional[StrokeData]: the StrokeData of the KeySequence. else None
    """
    if isinstance(data, KeySequence):
        return data.CovertToStrokeData()
    elif isinstance(data, StrokeData):
        return data
    elif isinstance(data, list):
        if (res := KeySequence(data)).IsValid():
            return res.CovertToStrokeData()
        elif (res := StrokeData(data)).IsValid():
            return res
    return None

# 获取插件快捷键元组列表
def GetPluginShortcuts(pluginID: int , print_console: bool = False) -> Optional[StrokeData]:
    """Retrieves the shortcuts for a plugin-id.

    Args:
        pid (int): The plugin id.

    Returns:
        list[list[tuple[int]]]: The shortcut sequences for the plugin.
    """
    # Get all shortcut containers for the plugin id.
    count = c4d.gui.GetShortcutCount()
    matches = [c4d.gui.GetShortcut(i) for i in range(count) if c4d.gui.GetShortcut(i)[c4d.SHORTCUT_PLUGINID] == pluginID]

    # build the shortcut data.
    result: list[StrokeData] = []
    for item in matches:
        sequence: list = []
        for i in range(0, c4d.SHORTCUT_PLUGINID, 10):
            index, shortcut = item[i], item[i+1]
            if isinstance(index, (int, float)):
                sequence.append((index, shortcut))
        if sequence != []:
            result.append(sequence)

    if print_console == True:
    # Output in console
        print("---------------")
        print("Plugin Name : {}".format(c4d.plugins.FindPlugin(pluginID).GetName()))             
        for item in result:
            for index, shortcut in item:                
                print (index, c4d.gui.Shortcut2String(index, shortcut))
        print("---------------")
    if result == []:
        result = None
    return result

# 获取快捷键全局序号(序号,不存在时返回False)
def GetIndex(keydata: KeyData, managerId: Optional[int] = None, pluginId: Optional[int] = None) -> Union[int, bool]:
    """Checks the #Index of given shortcut sequence, return False if not exsit."""
    strokeData: list[tuple[int, int]] = ToStrokeData(keydata)
    
    # Get the shortcut at #index.
    for index in range(c4d.gui.GetShortcutCount()):
        
        bc: c4d.BaseContainer = c4d.gui.GetShortcut(index)

        isMatch: bool = True
        for i, (qualifier, key) in enumerate(strokeData):
            idQualifier: int = i * 10 + 0
            idKey: int = i * 10 + 1
            # C4D中不存在此快捷键
            if bc[idQualifier] != qualifier or bc[idKey] != key:
                isMatch = False
                break

        # Something in the key sequence did not match with #strokeData, so we try the next shortcut
        # container provided by the outer loop.
        if not isMatch:
            continue
        
        # We could do here some additional tests, as shortcut key strokes do not have to be unique,
        # i.e., there could be two short-cuts "Shift + 1" bound to different manager contexts.
        if pluginId is not None and bc[c4d.SHORTCUT_PLUGINID] != pluginId:
            continue
        if managerId is not None and bc[c4d.SHORTCUT_ADDRESS] != managerId:
            continue
        
        # The shortcut was found.
        return index
    return False

# 获取包含此快捷键的序号列表
def GetAllIndexs(keydata: KeyData) -> list:
    """Return all the #Index of given shortcut sequence in a list."""
    strokeData: list[tuple[int, int]] = ToStrokeData(keydata)
    
    res = []
    # Get the shortcut at #index.
    for index in range(c4d.gui.GetShortcutCount()):        
        bc: c4d.BaseContainer = c4d.gui.GetShortcut(index)
        isMatch: bool = True
        for i, (qualifier, key) in enumerate(strokeData):
            idQualifier: int = i * 10 + 0
            idKey: int = i * 10 + 1
            # C4D中不存在此快捷键
            if bc[idQualifier] != qualifier or bc[idKey] != key:
                isMatch = False
                break
        if not isMatch:
            continue
        res.append(index)
    return res

# 删除快捷键    
def RemoveShortcut(keydata: KeyData, managerId: Optional[int] = None, pluginId: Optional[int] = None) -> bool:
    """Remove Shortcut by given KeyData"""
    if (index := GetIndex(keydata,managerId,pluginId)):
        return c4d.gui.RemoveShortcut(index)
    return False

# 获取快捷键指认的插件id
def GetAssignmentId(keydata: KeyData, managerId: Optional[int] = None) -> int:
    """Get assigned plugin id with given shortcut """
    res: list = []
    if managerId is None:
        indexs = GetAllIndexs(keydata)
        if len(indexs) == 0:
            return False
        for index in indexs:
            bc: c4d.BaseContainer = c4d.gui.GetShortcut(index)
            pluginId = bc[c4d.SHORTCUT_PLUGINID]
            res.append(pluginId)
        return res
    else:
        index = GetIndex(keydata,managerId)
        bc: c4d.BaseContainer = c4d.gui.GetShortcut(index)
        pluginId = bc[c4d.SHORTCUT_PLUGINID]
    return pluginId

# 获取快捷键指认管理器id
def GetManagerId(keydata: KeyData, pluginId: Optional[int] = None) -> int:
    """Finds a shortcut assigned plugin id and name"""
    res: list = []
    if pluginId is None:
        indexs = GetAllIndexs(keydata)
        if len(indexs) == 0:
            return False
        for index in indexs:
            bc: c4d.BaseContainer = c4d.gui.GetShortcut(index)
            managerId = bc[c4d.SHORTCUT_ADDRESS]
            if managerId != 0:
                res.append(managerId)
        return res
    else:
        index = GetIndex(keydata,pluginId=pluginId)
        bc: c4d.BaseContainer = c4d.gui.GetShortcut(index)
        managerId = bc[c4d.SHORTCUT_ADDRESS]
    return managerId

# 检测插件是否有指认的快捷键
def PluginHasShortcut(keydata: KeyData, pluginId: int) -> bool:
    """Check if shortcut binding with given plugin"""
    assigned_shortcut = GetPluginShortcuts(pluginId)
    if assigned_shortcut is None:
        return False
    given_shortcut = ToStrokeData(keydata)
    if len(assigned_shortcut) == 1 and assigned_shortcut[0] == given_shortcut: # 唯一
        return True
    if len(assigned_shortcut) > 1 and given_shortcut in assigned_shortcut: # 其中之一
        return True
    if not assigned_shortcut: # 没用指认快捷键
        return False
    else:
        return False

# 添加快捷键到对应的插件id和管理器id(可选)     
def AddShortCut(keydata: KeyData, pluginId, managerId: Optional[int] = 0) -> bool:
    """Add Shortcut by given qualifier and key to given ID"""
    if PluginHasShortcut(keydata, pluginId):
        return True
    strokeData: list[tuple[int, int]] = ToStrokeData(keydata)
    # Define shortcut container
    bc = c4d.BaseContainer()
    bc.SetInt32(c4d.SHORTCUT_PLUGINID, pluginId)
    bc.SetLong(c4d.SHORTCUT_ADDRESS, managerId)
    bc.SetLong(c4d.SHORTCUT_OPTIONMODE, 0)
    # User defined key
    for count, stroke in enumerate(strokeData): # [(5,83),(84)]
        if isinstance(stroke, tuple):
            bc.SetLong(count*10, stroke[0])
            bc.SetLong(count*10 + 1, stroke[1])
        elif isinstance(stroke, int):
            bc.SetLong(count*10, 0)
            bc.SetLong(count*10 + 1, 0)
    # Add shortcut
    return c4d.gui.AddShortcut(bc)

# 为插件添加快捷键(监测快捷键指认)
def SetPluginsShortcut(keydata: KeyData, pluginId:int, forced: bool = False) -> bool:
    if forced:
        return AddShortCut(keydata, pluginId)
    else:
        # 如果插件没有指认自定义快捷键
        if GetPluginShortcuts(pluginId) is None:
            # 如果全局快捷键中没有指定快捷键
            if not GetAssignmentId(keydata):
                return AddShortCut(keydata,pluginId)
        return False


