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
        Key_Locate: list = Key_Locate.split('.')
        Temp_Data: any = self.__Data_Toml
        for Temp_Key in Key_Locate:
            if type(Temp_Data) != dict: raise KeyError(Temp_Key)
            Temp_Data = Temp_Data[Temp_Key]
        return Temp_Data

    def Set_Value(self, Key_Locate: str, Value: any):
        '''
        It should be noted that when using Set_Value(), the modification of the Value accepted by Set_Value() will still affect the variables that are set_Value().
        需要注意的是, 在使用 Set_Value() 时, 对 Set_Value() 所接受的的 Value 的修改仍然会影响被Set_Value()的变量.
        Therefore, if you need to undo the reference relationship between Value and Data_Tomml, you need to perform deepcopy() operation on the variable represented by Value.
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

    def Add_Value(self, Key_Locate: str, Value: dict):
        Key_Locate: list = Key_Locate.split('.')
        Temp_Data: any = self.__Data_Toml
        for Temp_Key in Key_Locate:
            if type(Temp_Data) != dict: raise KeyError(Temp_Key)
            Temp_Data = Temp_Data[Temp_Key]
        Temp_Data.update(Value)
        self.Save_Toml()

    def POP_Key(self, Key_Locate: str):
        Key_Locate: list = Key_Locate.split('.')
        Temp_Data: any = self.__Data_Toml
        for Temp_Key in Key_Locate[:-1]:
            if type(Temp_Data) != dict: raise KeyError(Temp_Key)
            Temp_Data = Temp_Data[Temp_Key]
        Temp_Data.pop(Key_Locate[-1])
        self.Save_Toml()