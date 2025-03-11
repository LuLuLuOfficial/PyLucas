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
        return self.__Data_Toml.copy()

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

    def Set_Data_Basic(self, Data_Basic: dict):
        self.__Data_Toml = Data_Basic.copy()
        self.Save_Toml()

    def Set_Value(self, Key_Locate: str, Value: any):
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