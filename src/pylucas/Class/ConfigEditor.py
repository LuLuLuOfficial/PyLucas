import json, tomllib, tomli_w
from typing import Literal
from copy import deepcopy
from os.path import exists
from __future__ import annotations

class ConfigEditor():
    """_Make Config Great Again._
    """
    def __init__(self,
                 File: Literal['<Temporary>'],
                 Data: dict = {},
                 FileMode: Literal['toml', 'json'] = 'toml'):
        """_Make Config Great Again._

        Args:
            File (Literal['\<Temporary\>']): _description_
            Data (dict, optional): _description_. Defaults to {}.
            FileMode (Literal['toml', 'json'], optional): _description_. Defaults to 'toml'.
        """
        self.__Editor: ConfigEditor_Toml | ConfigEditor_Json

        match FileMode:
            case 'toml': self.__Editor = ConfigEditor_Toml(File=File, Data=Data)
            case 'json': self.__Editor = ConfigEditor_Json(File=File, Data=Data)
            case     _ : raise Exception('Target File Mode Not Support.')

    def ToDict(self) -> dict:
        return self.__Editor.ToDict()

    def DataCover(self, Data: dict) -> None:
        return self.__Editor.DataCover(Data=Data)

    def GetKeys(self, KeyLocate: str = '') -> tuple:
        return self.__Editor.GetKeys(KeyLocate=KeyLocate)

    def POPKey(self, KeyLocate: str) -> None:
        return self.__Editor.POPKey(KeyLocate=KeyLocate)

    def GetValue(self, KeyLocate: str) -> ConfigEditor | any:
        return self.__Editor.GetValue(KeyLocate=KeyLocate)

    def SetValue(self, KeyLocate: str, Value: any):
        return self.__Editor.SetValue(KeyLocate=KeyLocate, Value=Value)

    def AddValue(self, KeyLocate: str, Value: any):
        return self.__Editor.AddValue(KeyLocate=KeyLocate, Value=Value)

    def GetNestedPaths(self) -> list:
        return self.__Editor.GetNestedPaths()

class ConfigEditor_Basic():
    def __init__(self,
                 File: Literal['<Temporary>'],
                 Data: dict = {}):
        self._Temporary: bool = True if File == '<Temporary>' else False
        self._Flie: str = File
        self._Data: dict = deepcopy(Data) if self._Temporary else {}

        match self._Temporary:
            case True:
                return
            case False:
                if exists(File): self.Load()
                else: self.Save(File)

    def Initialize(self):
        pass

    def Load(self):
        if self._Temporary: return

    def Save(self, File: str = ''):
        if File:
            FileRoot: str = File[:File.rfind('\\')]
            if not exists(path=FileRoot):
                raise FileNotFoundError(rf"Path Root {FileRoot} not exists.")
            self._Temporary = False
            self._Flie = File
        if not self._Flie and self._Temporary: return

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
    """_下面的三个方法中的原变量和新变量不会存在任何引用关系._"""

    def GetValue(self, KeyLocate: str) -> ConfigEditor | any:
        KeyLocate: list = KeyLocate.split('.')
        TempData: any = self._Data
        for TempKey in KeyLocate:
            if not isinstance(TempData, dict): raise KeyError(f'{KeyLocate} -> {TempKey}')
            TempData = TempData[TempKey]
        if isinstance(TempData, dict): TempData: ConfigEditor = ConfigEditor(Data_Toml=TempData)
        else: pass
        return deepcopy(TempData)

    def SetValue(self, KeyLocate: str, Value: any):
        """_summary_

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
        TempData.update({KeyLocate[-1]: deepcopy(Value)})
        self.Save()

    def AddValue(self, KeyLocate: str, Value: any):
        """_summary_

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
                TempData.append(deepcopy(Value))
            case 'dict':
                if type(Value) != dict: raise TypeError(f'\'dict\' object Unable to Add a Element of {type(Value).__name__}')
                TempData.update(deepcopy(Value))
            case _:
                raise TypeError(f'\'{type(TempData).__name__}\' object UnSupport to AddElement')

        self.Save()

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

class ConfigEditor_Json(ConfigEditor_Basic):
    def Load(self) -> None:
        super().Load()
        with open(file=self._Flie, mode='r', encoding='utf-8') as File:
            self._Data = json.load(File)
            File.close()

    def Save(self, File: str = '') -> None:
        super().Save(File)
        with open(file=self._Flie, mode='w', encoding='utf-8') as File:
            json.dump(self._Data, File, ensure_ascii=False, indent=4)
            File.close()

class ConfigEditor_Toml(ConfigEditor_Basic):
    def Load(self) -> None:
        super().Load()
        with open(file=self._Flie, mode='rb') as File:
            self._Data = tomllib.load(File)
            File.close()

    def Save(self, File: str = '') -> None:
        super().Save(File)
        with open(file=self._Flie, mode='wb') as File:
            tomli_w.dump(self._Data, File)
            File.close()