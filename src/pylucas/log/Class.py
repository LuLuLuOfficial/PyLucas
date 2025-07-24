from os import mkdir, getcwd
from os.path import exists
from pathlib import Path as _Path
from typing import Literal
from sys import _getframe

from pylucas.function.Function import GetTimeStamp
from pylucas.log.Function import ASCII_Art

class LogManager():
    def __init__(self,
                 Author: str = None,
                 LogConsole: bool = True,
                 LogLimit: int = 10,
                 MsgLineBrk: bool = False,
                 OutPutPath_Root: str = r'.\Log') -> None:
        """_summary_

        Args:
            Author (str, optional): _Print the author's name in the log using AsciiArt._ Defaults to None.
            LogConsole (bool, optional): _Used to set whether to output in the console._ Defaults to True.
            LogLimit (int, optional): _Unlimited: LogLimit<0, Unsaved: LogLimit=0, Limited: LogLimit>0._ Defaults to 10.
            OutPutPath_Root (str, optional): _The root directory to save the log files._ Defaults to r'.\\Log'.
        """

        self.Author: str = Author
        self.LogConsole: bool = LogConsole
        self.LogLimit: int = LogLimit

        self.MsgLineBrk: bool = MsgLineBrk # 标记为弃用
        self.OutPutPath_Root: str = OutPutPath_Root
        self.OutPutPath_File: str = rf'{OutPutPath_Root}\{GetTimeStamp()}.log'

        self.WorkDir: str = getcwd() + '\\'

        self.CreateLogFile()
        self.CheckFileLimit()

    def __call__(self,
                 LogMessage: str = 'Invalid Information',
                 Level: Literal['Normal', 'Warn', 'Error'] = 'Normal',
                 Module: str = None,
                 LogConsole: Literal[None, True, False] = None):
        """_summary_

        Args:
            Module (str, optional): _Log Source._ Defaults By Auto Get.
            Level (Literal[Error, Warn, Normal], optional): _Log Level._ Defaults to 'Normal'.
            LogMessage (str, optional): _Log Output Message._ Defaults to 'Invalid Information'.
            LogConsole (bool, optional): _Whether the Log is output in the console._ Defaults is -1 mean fallow to self.LogConsole.
        """
        self.Log(LogMessage=LogMessage, Level=Level, Module=Module, LogConsole=LogConsole, From__Call__=True)

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
            self.Log(LogMessage = f'Deleted Oldest LogFile -> {OldestFile}.', Module='LogManager.CheckFileLimit')
            Files = [f for f in Path.iterdir() if f.is_file() and f.suffix.lower() == '.log']

    def Log(self,
            LogMessage: str = 'Invalid Information',
            Level: Literal['Normal', 'Warn', 'Error'] = 'Normal',
            Module: str = None,
            LogConsole: Literal[None, True, False] = None,
            From__Call__: bool = False):
        """_summary_

        Args:
            Module (str, optional): _Log Source._ Defaults By Auto Get.
            Level (Literal[Error, Warn, Normal], optional): _Log Level._ Defaults to 'Normal'.
            LogMessage (str, optional): _Log Output Message._ Defaults to 'Invalid Information'.
            LogConsole (bool, optional): _Whether the Log is output in the console._ Defaults is -1 mean fallow to self.LogConsole.
        """
        TimeStamp: str = GetTimeStamp()
        Level: str = Level
        if Module is None:
            if From__Call__: Module = self.GetStack(3)
            else: Module = self.GetStack(2)
        LogMessage: str = LogMessage[:-1] if LogMessage[-1] in ['.', '。'] else LogMessage

        Message: str = f'{TimeStamp} |-| [Level: <{Level}> | Module: <{Module}>]:\n  LogMessage: {LogMessage}.'

        if (self.LogConsole if LogConsole == None else LogConsole): print(Message)

        if not self.LogLimit: return
        with open(file=self.OutPutPath_File, mode='a', encoding='utf-8') as LogFile:
            LogFile.write(f'{Message}\n')
            LogFile.close()

    def GetStack(self, Level: int | None):
        Frame = _getframe(Level)
        CurrentFile = Frame.f_code.co_filename.replace(self.WorkDir, '')
        Modules = []
        while Frame:
            Name = Frame.f_code.co_name
            if Name == '<module>': break
            _Self = Frame.f_locals.get('self')
            _Class = Frame.f_locals.get('cls')
            if _Self or _Class:
                class_name = (_Self.__class__.__name__ if _Self else _Class.__name__)
                Name = f"{class_name}::{Name}"
            Modules.append(Name)
            Frame = Frame.f_back
        return f"{CurrentFile}|{'.'.join(reversed(Modules))}"

