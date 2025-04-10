from __future__ import annotations
import tomllib, tomli_w

class ConfigEditor():
    def __init__(self, Path_Toml: str, Data_Toml: dict = {}):
        '''
        Path_Toml: str = 'Temporary' | 'Any Exists Path'
        Data_Toml: dict = {...}
        '''
        self.__Path_Toml: str = ''
        self.__Data_Toml: dict = {}
        self.Temporary: bool = False

        self.Initialize(Path_Toml=Path_Toml, Data_Toml=Data_Toml)

    def Initialize(self, Path_Toml: str, Data_Toml: dict):
        from os.path import exists
        match Path_Toml:
            case 'Temporary':
                self.Temporary = True
                self.Set_Data_Toml(Data_Toml=Data_Toml)
            case _:
                match exists(self.__Path_Toml):
                    case True:
                        self.Load_Toml()
                    case False:
                        self.Save_Toml()

    # Pair --------------------------------------------------
    def Load_Toml(self) -> None:
        if self.Temporary: return
        with open(file=self.__Path_Toml, mode='rb') as File_Toml:
            self.__Data_Toml = tomllib.load(File_Toml)
            File_Toml.close()

    def Save_Toml(self, FiledPath: str = '') -> None:
        if FiledPath and self.Temporary:
            self.Temporary = False
            self.__Path_Toml = FiledPath
        if self.Temporary: return
        with open(file=self.__Path_Toml, mode='wb') as File_Toml:
            tomli_w.dump(self.__Data_Toml, File_Toml)
            File_Toml.close()

    # Pair --------------------------------------------------
    '''
    下面的三个方法中的原变量和新变量不会存在任何引用关系.
    '''
    def Get_Data_Toml(self) -> dict:
        from copy import deepcopy
        return deepcopy(self.__Data_Toml)

    def Set_Data_Toml(self, Data_Toml: dict) -> None:
        '''
        仅在 self.__Data_Toml 为空或任何 bool(self.__Data_Toml)!=True 情况下有效
        不建议使用这个方法
        '''
        from copy import deepcopy
        if self.__Data_Toml:
            return
        self.__Data_Toml = deepcopy(Data_Toml)
        self.Save_Toml()

    def OverWrite_Data(self, Data_Toml: dict):
        '''
        强制覆写 self.__Data_Toml
        不建议使用这个方法
        '''
        from copy import deepcopy
        self.__Data_Toml = deepcopy(Data_Toml)
        self.Save_Toml()

    # Pair --------------------------------------------------
    '''
    下面的三个方法中的原变量和新变量不会存在任何引用关系.
    '''
    def Get_Keys(self, Key_Locate: str = '') -> tuple:
        Key_Locate: list = Key_Locate.split('.')
        Temp_Data: any = self.__Data_Toml
        if Key_Locate[0]:
            for Temp_Key in Key_Locate:
                if type(Temp_Data) != dict: raise KeyError(f'{Key_Locate} -> {Temp_Key}')
                Temp_Data = Temp_Data[Temp_Key]

        return tuple(Temp_Data.keys())

    def Set_Key(self, Key_Locate: str, New_Key: str) -> None:
        pass

    def POP_Key(self, Key_Locate: str):
        Key_Locate: list = Key_Locate.split('.')
        Temp_Data: any = self.__Data_Toml
        for Temp_Key in Key_Locate[:-1]:
            if type(Temp_Data) != dict: raise KeyError(f'{Key_Locate} -> {Temp_Key}')
            Temp_Data = Temp_Data[Temp_Key]
        Temp_Data.pop(Key_Locate[-1])
        self.Save_Toml()

    # Pair --------------------------------------------------
    '''
    下面的三个方法中的原变量和新变量仍然存在引用关系.
    '''
    def Get_Value(self, Key_Locate: str) -> ConfigEditor | any:
        Key_Locate: list = Key_Locate.split('.')
        Temp_Data: any = self.__Data_Toml
        for Temp_Key in Key_Locate:
            if type(Temp_Data) != dict: raise KeyError(f'{Key_Locate} -> {Temp_Key}')
            Temp_Data = Temp_Data[Temp_Key]
        match type(Temp_Data).__name__:
            case 'dict':
                Temp_Data: ConfigEditor = ConfigEditor(Path_Toml='Temporary', Data_Toml=Temp_Data)
            case _:
                pass
        return Temp_Data

    def Set_Value(self, Key_Locate: str, Value: any) -> None:
        '''
        The key path indicated by Key_Locate in the Set_Value requirement may not exist in Data_Toml.
        在 Set_Value 的要求中 Key_Locate 所指示的键路径可以不存在于 Data_Toml 中.
        In the implementation of Set_Value, Set_Value will directly overwrite the Value into the Value of the key-value pair indicated by Key_Locate.
        在 Set_Value 的实现中 Set_Value 会将 Value 直接覆盖到 Key_Locate 所指示的键值对的 Value 中.
        '''
        Key_Locate: list = Key_Locate.split('.')
        Temp_Data: any = self.__Data_Toml
        for Temp_Key in Key_Locate[:-1]:
            if type(Temp_Data) == dict:
                if Temp_Key in Temp_Data:
                    Temp_Data = Temp_Data[Temp_Key]
                else:
                    Temp_Data.update({Temp_Key: {}})
                    Temp_Data = Temp_Data[Temp_Key]
            else:
                raise TypeError(f'Temp_Data: {type(Temp_Data)} = {Temp_Data}')
        Temp_Data.update({Key_Locate[-1]: Value})
        self.Save_Toml()

    def Add_Value(self, Key_Locate: str, Value: any) -> None:
        '''
        The key path indicated by Key_Locate in the requirements of Add_Value must exist in Data_Toml.
        在 Add_Value 的要求中 Key_Locate 所指示的键路径必须存在于 Data_Toml 中.
        In the implementation of Add_Value Add_Value only adds Value to the Value of the key-value pair indicated by Key_Locate.
        在 Add_Value 的实现中 Add_Value 仅会将 Value 添加到 Key_Locate 所指示的键值对的 Value 中.
        '''
        Key_Locate: list = Key_Locate.split('.')
        Temp_Data: any = self.__Data_Toml
        for Temp_Key in Key_Locate:
            if type(Temp_Data) != dict: raise KeyError(f'{Key_Locate} -> {Temp_Key}')
            Temp_Data = Temp_Data[Temp_Key]
        match type(Temp_Data).__name__:
            case 'int':
                raise TypeError('\'int\' object Unable to Add Element')
            case 'float':
                raise TypeError('\'float\' object Unable to Add Element')
            case 'str':
                raise TypeError('\'str\' object Unable to Add Element')
            case 'tuple':
                raise TypeError('\'tuple\' object Unable to Add Element')
            case 'list':
                Temp_Data.append(Value)
            case 'dict':
                if type(Value) != dict: raise TypeError(f'\'dict\' object Unable to Add a Element of {type(Value).__name__}')
                Temp_Data.update(Value)
            case _:
                raise TypeError(f'\'{type(Temp_Data).__name__}\' object UnSupport to AddElement')

        self.Save_Toml()