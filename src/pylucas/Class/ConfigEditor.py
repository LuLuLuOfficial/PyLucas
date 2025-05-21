from __future__ import annotations # 解决类型注解中的引用问题, 必须放在首位导入
import json, tomllib, tomli_w
from typing import Literal
from copy import deepcopy
from os.path import exists, normpath

class ConfigEditor():
    def __init__(self,
                 File: Literal['<Temporary>'],
                 Data: dict = {}):
        self._Temporary: bool = True if File == '<Temporary>' else False
        self._Flie: str = normpath(File)
        self._Data: dict = deepcopy(Data)

        FileMode: str = self._Flie.split('.')[-1].upper() if not self._Temporary else 'TOML'
        match FileMode:
            case 'TOML':
                self._SL = ConfigEditorSL_Toml(Temporary=self._Temporary, File=self._Flie)
            case 'JSON':
                self._SL = ConfigEditorSL_Json(Temporary=self._Temporary, File=self._Flie)
            case     _ : raise Exception('Target File Mode Not Support.')

        match self._Temporary:
            case True:
                return
            case False:
                if exists(File): self.Load()
                else: self.Save(File)

    def __repr__(self):
        return str(self.ToDict)

    def Initialize(self):
        pass

    def Load(self):
        self._Data = self._SL.Load()

    def Save(self, File: str = ''):
        self._SL.Save(Data=self._Data, File=File)

    # Pair --------------------------------------------------
    """_下面的两个方法中的原变量和新变量不会存在任何引用关系._"""
    @property
    def ToDict(self) -> dict:
        from copy import deepcopy
        return deepcopy(self._Data)

    def DataCover(self, Data: dict) -> None:
        """_强制使用深拷贝覆写 self._Data, 不建议使用这个方法._

        Args:
            Data (dict): _description_
        """
        from copy import deepcopy
        self._Data = deepcopy(Data)
        self.Save()

    # Pair --------------------------------------------------

    def GetKeys(self, KeyLocate: str = '') -> tuple:
        KeyLocate: list = KeyLocate.split('.')
        TempData: any = self._Data
        Keys: tuple = ()
        if KeyLocate == ['']: KeyLocate = []
        for TempKey in KeyLocate:
            if not isinstance(TempData, dict): raise KeyError(f'{KeyLocate} -> {TempKey}')
            TempData = TempData[TempKey]
        if isinstance(TempData, dict): Keys = tuple(TempData.keys())
        else: Keys = ()

        return Keys

    def POPKey(self, KeyLocate: str) -> None:
        KeyLocate: list = KeyLocate.split('.')
        TempData: any = self._Data
        for TempKey in KeyLocate[:-1]:
            if not isinstance(TempData, dict): raise KeyError(f'{KeyLocate} -> {TempKey}')
            TempData = TempData[TempKey]
        TempData.pop(KeyLocate[-1])
        self.Save()

    # Pair --------------------------------------------------
    """_下面的三个方法中的原变量和新变量仍存在引用关系._"""

    def GetValue(self,
                 KeyLocate: str,
                 ResultType: Literal['ConfigEditor', 'Self'] = 'ConfigEditor') -> ConfigEditor | any:
        """_获取键值, 键值与源字典存在引用关系._

        Args:
            KeyLocate (str): _description_
            ResultType (Literal['ConfigEditor', 'Self'], optional): _description_. Defaults to 'ConfigEditor'.

        Raises:
            KeyError: _description_

        Returns:
            ConfigEditor | any: _description_
        """
        KeyLocate: list = KeyLocate.split('.')
        TempData: any = self._Data
        for TempKey in KeyLocate:
            if not isinstance(TempData, dict): raise KeyError(f'{KeyLocate} -> {TempKey}')
            TempData = TempData[TempKey]
        if isinstance(TempData, dict) and ResultType == 'ConfigEditor': TempData: ConfigEditor = ConfigEditor(File='<Temporary>', Data=TempData)
        else: pass
        return TempData

    def SetValue(self, KeyLocate: str, Value: any):
        """_写入键值, 键值与目标字典存在引用关系._

        Args:
            KeyLocate (str): _KeyLocate 所指示的键路径可以不存在于 self._Data 中._
            Value (any): _description_

        Raises:
            TypeError: _description_
        """
        KeyLocate: list = KeyLocate.split('.')
        TempData: any = self._Data
        for TempKey in KeyLocate[:-1]:
            if isinstance(TempData, dict):
                if TempKey in TempData:
                    TempData = TempData[TempKey]
                else:
                    TempData.update({TempKey: {}})
                    TempData = TempData[TempKey]
            else:
                raise TypeError(f'TempData: {type(TempData)} = {TempData}')
        TempData.update({KeyLocate[-1]: Value})
        self.Save()

    def AddValue(self, KeyLocate: str, Value: any):
        """_向可迭代键值中添加元素, 元素与目标字典存在引用关系._

        Args:
            KeyLocate (str): _KeyLocate 所指示的键路径必须存在于 self._Data 中._
            Value (any): _description_

        Raises:
            KeyError: _KeyLocate 所指示的键路径不存在于 self.__Data中._
            TypeError: _\'UnSupport Type\' object Unable to Add Element._
        """
        KeyLocate: list = KeyLocate.split('.')
        TempData: any = self._Data
        for TempKey in KeyLocate:
            if not isinstance(TempData, dict): raise KeyError(f'{KeyLocate} -> {TempKey}')
            TempData = TempData[TempKey]
        match type(TempData).__name__:
            case 'int':
                raise TypeError('\'int\' object Unable to Add Element')
            case 'float':
                raise TypeError('\'float\' object Unable to Add Element')
            case 'str':
                raise TypeError('\'str\' object Unable to Add Element')
            case 'tuple':
                raise TypeError('\'tuple\' object Unable to Add Element')
            case 'list':
                TempData.append(Value)
            case 'dict':
                if type(Value) != dict: raise TypeError(f'\'dict\' object Unable to Add a Element of {type(Value).__name__}')
                TempData.update(Value)
            case _:
                raise TypeError(f'\'{type(TempData).__name__}\' object UnSupport to AddElement')

        self.Save()

    # Pair --------------------------------------------------

    def GetNestedPaths(self, KeyLocate: str = '') -> list:
        NestedPaths: list = []
        def DepthRecursion(KeyLocate: str):
            Keys: list = self.GetKeys(KeyLocate=KeyLocate)
            for Key in Keys:
                if KeyLocate == '': KeyLocate_Sub: str = f'{Key}'
                else: KeyLocate_Sub: str = f'{KeyLocate}.{Key}'
                SubKeys = self.GetKeys(KeyLocate=KeyLocate_Sub)
                if SubKeys: DepthRecursion(KeyLocate=KeyLocate_Sub)
                else: NestedPaths.append([KeyLocate, Key])
        DepthRecursion(KeyLocate)
        return NestedPaths

class ConfigEditorSL():
    def __init__(self,
                 Temporary: bool,
                 File: str):
        self._Temporary: bool = Temporary
        self._Flie: str = File

    def Load(self) -> dict:
        pass

    def Save(self, Data: dict, File: str = '') -> None:
        if File:
            FileRoot: str = normpath(File)
            FileRoot: str = FileRoot[FileRoot.rfind('\\')]
            if not exists(path=FileRoot):
                raise FileNotFoundError(rf"Path Root {FileRoot} not exists.")
            self._Temporary = False
            self._Flie = File
        if not self._Flie and self._Temporary: return

class ConfigEditorSL_Toml(ConfigEditorSL):
    def __init__(self, Temporary, File):
        super().__init__(Temporary, File)

    def Load(self) -> dict:
        with open(file=self._Flie, mode='rb') as File:
            Data = tomllib.load(File)
            File.close()
        return Data

    def Save(self, Data: dict, File: str = '') -> None:
        super().Save(File)
        with open(file=self._Flie, mode='wb') as File:
            tomli_w.dump(Data, File)
            File.close()

class ConfigEditorSL_Json(ConfigEditorSL):
    def __init__(self, Temporary, File):
        super().__init__(Temporary, File)

    def Load(self) -> dict:
        with open(file=self._Flie, mode='r', encoding='utf-8') as File:
            Data = json.load(File)
            File.close()
        return Data

    def Save(self, Data: dict, File: str = '') -> None:
        super().Save(File)
        with open(file=self._Flie, mode='w', encoding='utf-8') as File:
            json.dump(Data, File, ensure_ascii=False, indent=4)
            File.close()
