import tomllib, tomli_w

class ConfigEditor():
    def __init__(self, Path_Toml: str):
        self.__Path_Toml: str = Path_Toml
        self.__Data_Toml: dict = {}

        self.Initialize()

    def Initialize(self):
        from os.path import exists
        match exists(self.__Path_Toml):
            case True:
                self.Load_Toml()
            case False:
                self.Save_Toml()

    def Load_Toml(self):
        with open(file=self.__Path_Toml, mode='rb') as File_Toml:
            self.__Data_Toml = tomllib.load(File_Toml)
            File_Toml.close()

    def Save_Toml(self):
        with open(file=self.__Path_Toml, mode='wb') as File_Toml:
            tomli_w.dump(self.__Data_Toml, File_Toml)
            File_Toml.close()

    @property
    def Get_Data_Toml(self):
        from copy import deepcopy
        return deepcopy(self.__Data_Toml)

    def Get_Keys(self, Key_Locate: str = ''):
        Key_Locate: list = Key_Locate.split('.')
        Temp_Data: any = self.__Data_Toml
        if Key_Locate[0]:
            for Temp_Key in Key_Locate:
                if type(Temp_Data) != dict: raise KeyError(Temp_Key)
                Temp_Data = Temp_Data[Temp_Key]

        return tuple(Temp_Data.keys())
            

    def Get_Value(self, Key_Locate: str):
        '''
        It should be noted that when using Get_Value(), there is still a reference relationship between the returned Temp_Data and Data_Toml.
        需要注意的是, 在使用 Get_Value() 时, 返回的 Temp_Data 与 Data_Toml 之间仍然存在引用关系.
        Therefore, if you need to undo the reference relationship between Temp_Data and Data_Toml, you need to perform deepcopy() operation on Temp_Data.
        所以, 如果需要解除 Temp_Data 与 Data_Toml 之间的引用关系, 需要对 Temp_Data 进行 deepcopy() 操作.
        '''
        Key_Locate: list = Key_Locate.split('.')
        Temp_Data: any = self.__Data_Toml
        for Temp_Key in Key_Locate:
            if type(Temp_Data) != dict: raise KeyError(Temp_Key)
            Temp_Data = Temp_Data[Temp_Key]
        return Temp_Data

    def Set_Value(self, Key_Locate: str, Value: any):
        '''
        The key path indicated by Key_Locate in the Set_Value requirement may not exist in Data_Toml.
        在 Set_Value 的要求中 Key_Locate 所指示的键路径可以不存在于 Data_Toml 中.
        In the implementation of Set_Value, Set_Value will directly overwrite the Value into the Value of the key-value pair indicated by Key_Locate.
        在 Set_Value 的实现中 Set_Value 会将 Value 直接覆盖到 Key_Locate 所指示的键值对的 Value 中.

        It should be noted that after using Set_Value(), there is still a reference relationship between the variable represented by Value and Data_Toml.
        需要注意的是, 在使用 Set_Value() 后, Value 所代表的变量与 Data_Toml 之间仍然存在引用关系.
        Therefore, if you need to undo the reference relationship between Value and Data_Toml, you need to perform deepcopy() operation on the variable represented by Value.
        所以, 如果需要解除 Value 与 Data_Toml 之间的引用关系, 需要对 Value 所代表的变量进行 deepcopy() 操作.
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

    def Set_Data_Basic(self, Data_Toml: dict):
        '''
        仅在 self.__Data_Toml 为空或任何 bool(self.__Data_Toml)!=True 情况下有效
        '''
        from copy import deepcopy
        if self.__Data_Toml:
            return
        self.__Data_Toml = deepcopy(Data_Toml)
        self.Save_Toml()

    def OverWrite_Data(self, Data_Toml: dict):
        from copy import deepcopy
        self.__Data_Toml = deepcopy(Data_Toml)
        self.Save_Toml()

    def Add_Value(self, Key_Locate: str, Value: any):
        '''
        The key path indicated by Key_Locate in the requirements of Add_Value must exist in Data_Toml.
        在 Add_Value 的要求中 Key_Locate 所指示的键路径必须存在于 Data_Toml 中.
        In the implementation of Add_Value Add_Value only adds Value to the Value of the key-value pair indicated by Key_Locate.
        在 Add_Value 的实现中 Add_Value 仅会将 Value 添加到 Key_Locate 所指示的键值对的 Value 中.
        '''
        Key_Locate: list = Key_Locate.split('.')
        Temp_Data: any = self.__Data_Toml
        for Temp_Key in Key_Locate:
            if type(Temp_Data) != dict: raise KeyError(Temp_Key)
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

    def POP_Key(self, Key_Locate: str):
        Key_Locate: list = Key_Locate.split('.')
        Temp_Data: any = self.__Data_Toml
        for Temp_Key in Key_Locate[:-1]:
            if type(Temp_Data) != dict: raise KeyError(Temp_Key)
            Temp_Data = Temp_Data[Temp_Key]
        Temp_Data.pop(Key_Locate[-1])
        self.Save_Toml()