from os.path import exists
from os import mkdir
from pathlib import Path as _Path
from inspect import stack
from pylucas.Function.Function import ASCII_Art, GetTimeStamp
from typing import Literal

class LogManager():
    """_summary_
    """
    def __init__(self, OutPutPath_Root: str, Author: str = None) -> None:
        self.Author: str = Author
        self.TimeStamp: str = ''
        self.OutPutPath_Root: str = OutPutPath_Root
        self.OutPutPath_File: str = OutPutPath_Root

        self.MessageLineBreak: bool = False
        self.LogLimit: list[bool, int] = [True, 10]

        self.Initialize()

    def Initialize(self):
        if not exists(self.OutPutPath_Root): mkdir(self.OutPutPath_Root)

        self.TimeStamp = GetTimeStamp()
        self.OutPutPath_File += rf'\{self.TimeStamp}.txt'
        with open(file=self.OutPutPath_File, mode='w', encoding='utf-8') as file:
            if self.Author:
                FormatText, LineCount = ASCII_Art(Text=self.Author)
                file.write(f'{FormatText}')
                file.write(f'Log File Created At {self.TimeStamp}'+'\n'*(10-(LineCount%10)))
            else:
                file.write(f'Log File Created At {self.TimeStamp}'+'\n'*9)
            file.close()
        self.CheckLogLimit()
    
    def SetLogLimit(self, Mode: bool, Limit: int = None):
        if not Limit: self.LogLimit[0] = Mode
        self.LogLimit = [Mode, Limit]

    def SetMessageLB(self, Mode: bool):
        if Mode: self.MessageLineBreak = True
        else: self.MessageLineBreak = False

    def CheckLogLimit(self):
        Path = _Path(self.OutPutPath_Root)
        Files = [f for f in Path.iterdir() if f.is_file() and f.suffix.lower() == '.txt']
        if not Files:
            return
        while (self.LogLimit[0]) and (len(Files) > self.LogLimit[1]):
            OldestFile = min(Files, key=lambda f: f.stat().st_mtime)
            self.LogOutput(LogMessage = f'Deleted Oldest LogFile -> {OldestFile}.')
            OldestFile.unlink()
            Files = [f for f in Path.iterdir() if f.is_file() and f.suffix.lower() == '.txt']

    def LogOutput(self,
                  Module: str = None,
                  Level: Literal['Normal', 'Warn', 'Error'] = 'Normal',
                  LogMessage: str = 'Invalid Information',
                  DoPrint: bool = True):
        '''
        Module: str = 'By Auto'
        Level: str = 'Error' | 'Warn' | 'Normal'
        LogMessage: str = 'Invalid Information.'
        DoPrint: bool = True | False
        '''
        if not Module: Module = stack()[1][0].f_globals['__name__']
        TimeStamp = GetTimeStamp()
        Indent: str = ''
        if self.MessageLineBreak: Indent = '\n\t'
        else: Indent = ' '
        if LogMessage[-1] in ('.', '。',): LogMessage = LogMessage[:-1]

        LogText: str = f'{TimeStamp} |-| [Level: <{Level}> | Module: <{Module}>]:{Indent}{LogMessage}.'
        
        if DoPrint:
            print(LogText)
        with open(file=self.OutPutPath_File, mode='a', encoding='utf-8') as file:
            file.write(f'{LogText}\n')