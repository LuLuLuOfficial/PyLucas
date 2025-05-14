from os.path import exists
from os import mkdir
from pathlib import Path as _Path
from inspect import stack
from pylucas.Function.Function import ASCII_Art, GetTimeStamp
from typing import Literal

class LogManager():
    def __init__(self,
                 Author: str = None,
                 LogConsole: bool = True,
                 LogLimit: list[bool | int] | int = 10,
                 MsgLineBrk: bool = False,
                 OutPutPath_Root: str = r'.\Log') -> None:
        """_summary_

        Args:
            Author (str, optional): _Print the author's name in the log using AsciiArt._ Defaults to None.
            LogConsole (bool, optional): _Used to set whether to output in the console._ Defaults to True.
            LogLimit (int, optional): _Unlimited: LogLimit<0, Unsaved: LogLimit=0, Limited: LogLimit>0._ Defaults to 10.
            OutPutPath_Root (str, optional): _The root directory to save the log files._ Defaults to r'.\Log'.
        """
        
        self.Author: str = Author
        self.LogConsole: bool = LogConsole
        self.LogLimit: list[bool | int] | int = LogLimit

        if type(LogLimit).__name__ == 'list': # This Patr Will Be Discard In Next Major Version.
            if LogLimit[0] == False: self.LogLimit = -1
            else: self.LogLimit = LogLimit[1]

        self.MsgLineBrk: bool = MsgLineBrk
        self.OutPutPath_Root: str = OutPutPath_Root
        self.OutPutPath_File: str = rf'{OutPutPath_Root}\{GetTimeStamp()}.log'

        

        self.Initialize()

    def Initialize(self):
        self.CreateLogFile()
        self.CheckFileLimit()
    
    def CreateLogFile(self):
        if not self.LogLimit: return

        if not exists(self.OutPutPath_Root): mkdir(self.OutPutPath_Root)
        if self.Author:
            FormatText, LineCount = ASCII_Art(Text=self.Author, AddSplit=True)
            CreatedLog: str = f'Log File Created At {GetTimeStamp()}'+'\n'*(10-(LineCount%10))
        else:
            FormatText: str = ''
            CreatedLog: str = f'Log File Created At {GetTimeStamp()}'+'\n'*10
        with open(file=self.OutPutPath_File, mode='w', encoding='utf-8', ) as LogFile:
            LogFile.write(f'{FormatText}{CreatedLog}')
            LogFile.close()

    def CheckFileLimit(self):
        if self.LogLimit <= 0: return
        
        Path = _Path(self.OutPutPath_Root)
        Files = [f for f in Path.iterdir() if f.is_file() and f.suffix.lower() == '.log']
        if not Files: return
        while len(Files) > self.LogLimit:
            OldestFile = min(Files, key=lambda f: f.stat().st_mtime)
            OldestFile.unlink()
            self.Log(LogMessage = f'Deleted Oldest LogFile -> {OldestFile}.')
            Files = [f for f in Path.iterdir() if f.is_file() and f.suffix.lower() == '.log']

    def SetLogLimit(self, Mode: bool, Limit: int = None): # This Func Will Be Discard In Next Major Version.
        if Mode == False: self.LogLimit = -1
        elif Limit: self.LogLimit = Limit

    def SetMessageLB(self, Mode: bool): # This Func Will Be Discard In Next Major Version.
        """This Func Will Be Discard In Next Major Version.

        Args:
            Mode (bool): _description_
        """
        if Mode: self.MsgLineBrk = True
        else: self.MsgLineBrk = False

    def LogOutput(self, # This Func Will Be Discard In Next Major Version.
                  Module: str = None,
                  Level: Literal['Normal', 'Warn', 'Error'] = 'Normal',
                  LogMessage: str = 'Invalid Information',
                  DoPrint: Literal[None, True, False] = None):
        """This Func Will Be Discard In Next Major Version.

        Args:
            Module (str, optional): _Log Source._ Defaults By Auto Get.
            Level (Literal[Error, Warn, Normal], optional): _Log Level._ Defaults to 'Normal'.
            LogMessage (str, optional): _Log Output Message._ Defaults to 'Invalid Information'.
            DoPrint (bool, optional): _Whether the Log is output in the console._ Defaults fallow to self.LogConsole.
        """
        self.Log(Module=Module,
                 Level=Level,
                 LogMessage=LogMessage,
                 LogConsole=DoPrint)

    def Log(self,
            Module: str = None,
            Level: Literal['Normal', 'Warn', 'Error'] = 'Normal',
            LogMessage: str = 'Invalid Information',
            LogConsole: Literal[None, True, False] = None):
        """_summary_

        Args:
            Module (str, optional): _Log Source._ Defaults By Auto Get.
            Level (Literal[Error, Warn, Normal], optional): _Log Level._ Defaults to 'Normal'.
            LogMessage (str, optional): _Log Output Message._ Defaults to 'Invalid Information'.
            LogConsole (bool, optional): _Whether the Log is output in the console._ Defaults is -1 mean fallow to self.LogConsole.
        """
        TimeStamp: str = GetTimeStamp()
        Level: str = Level
        Module = Module if Module else stack()[1][0].f_globals['__name__']
        Indent: str = '\n\t' if self.MsgLineBrk else ' '
        LogMessage: str = LogMessage[:-1] if LogMessage[-1] in ['.', '。'] else LogMessage

        Message: str = f'{TimeStamp} |-| [Level: <{Level}> | Module: <{Module}>]:{Indent}{LogMessage}.'

        if (self.LogConsole if LogConsole == None else LogConsole): print(Message)

        if not self.LogLimit: return
        with open(file=self.OutPutPath_File, mode='a', encoding='utf-8') as LogFile:
            LogFile.write(f'{Message}\n')
            LogFile.close()