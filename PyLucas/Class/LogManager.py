from os.path import exists
from os import mkdir
from pathlib import Path as _Path
from inspect import stack
from PyLucas.Func.Function import Author_Lucas, GetTimeStamp

class LogManager():
    def __init__(self, OutPutPath_Root) -> None:
        self.TimeStamp: str = ''
        self.OutPutPath_Root: str = OutPutPath_Root
        self.OutPutPath_File: str = OutPutPath_Root

        self.MassageLineBreak: bool = False
        self.LogLimit: list[bool, int] = [True, 10]

        self.Initialize()

    def Initialize(self):
        if not exists(self.OutPutPath_Root): mkdir(self.OutPutPath_Root)

        self.TimeStamp = GetTimeStamp()
        self.OutPutPath_File += rf'\{self.TimeStamp}.txt'
        with open(file=self.OutPutPath_File, mode='w', encoding='utf-8') as file:
            file.write(100 * '-' + '\n')
            file.write(f'{Author_Lucas()}')
            file.write(100 * '-' + '\n')
            file.write(f'Log File Created At {self.TimeStamp}\n\n\n\n\n')
            file.close()
        self.CheckLogLimit()
    
    def SetLogLimit(self, Mode: bool, Limit: int = None):
        if not Limit: self.LogLimit[0] = Mode
        self.LogLimit = [Mode, Limit]

    def SetMassageLB(self, Mode: bool):
        if Mode: self.MassageLineBreak = True
        else: self.MassageLineBreak = False

    def CheckLogLimit(self):
        Path = _Path(self.OutPutPath_Root)
        Files = [f for f in Path.iterdir() if f.is_file() and f.suffix.lower() == '.txt']
        if not Files:
            return
        while (self.LogLimit[0]) and (len(Files) > self.LogLimit[1]):
            OldestFile = min(Files, key=lambda f: f.stat().st_mtime)
            self.LogOutput(LogMassage = f'Deleted Oldest LogFile -> {OldestFile}.')
            OldestFile.unlink()
            Files = [f for f in Path.iterdir() if f.is_file() and f.suffix.lower() == '.txt']

    def LogOutput(self, Module: str = None, Level: str = 'Normal', LogMassage: str = 'Invalid Information', DoPrint: bool = True):
        '''
        Module: str = 'By Auto'
        Level: str = 'Error' | 'Warn' | 'Normal'
        LogMassage: str = 'Invalid Information.'
        DoPrint: bool = True | False
        '''
        if not Module: Module = stack()[1][0].f_globals['__name__']
        TimeStamp = GetTimeStamp()
        Indent: str = ''
        if self.MassageLineBreak: Indent = '\n\t'
        else: Indent = ' '
        if LogMassage[-1] in ('.', '。',): LogMassage = LogMassage[:-1]

        LogText: str = f'{TimeStamp} |-| [Level: <{Level}> | Module: <{Module}>]:{Indent}{LogMassage}.'
        
        if DoPrint:
            print(LogText)
        with open(file=self.OutPutPath_File, mode='a', encoding='utf-8') as file:
            file.write(f'{LogText}\n')