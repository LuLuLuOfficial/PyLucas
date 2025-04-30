'''
------------------------------
    Command-Line Interface
          命令行界面
------------------------------
'''
from re import compile
from typing import Type
from inspect import getmembers, ismethod
from time import sleep as LoopPause
from copy import deepcopy

from pylucas.Function import ASCII_Art
from pylucas import ConfigEditor
from pylucas.Class.DualCaseSet import DualCaseSet

def ConsoleLog(*values: object,):
    print('Console: ', end='')
    for value in values:
        print(value, end=' ')
    print()

def CommandsToHelp(Commands: ConfigEditor, CommandsOrder: tuple) -> list:
    TempList: list = []
    # Depth Recursion
    def DepthRecursion(Key_Locate: str):
        SubKeys_1: list = Commands.Get_Keys(Key_Locate=Key_Locate)
        for SubKey_1 in SubKeys_1:
            SubKey_Locate: str = f'{Key_Locate}.{SubKey_1}'
            SubKeys_2 = Commands.Get_Keys(Key_Locate=SubKey_Locate)
            if SubKeys_2: DepthRecursion(Key_Locate=SubKey_Locate)
            else: TempList.append([Key_Locate, SubKey_1, Commands.Get_Value(SubKey_Locate)])
    # Handle
    for Key in CommandsOrder: DepthRecursion(Key_Locate=Key)
    # Format
    EndList: list = []
    Temp_Tittle: str = ''
    Temp_Command: str = ''
    for Index, Result in enumerate(TempList):
        Temp_Tittle = ''
        Temp_Command = ''
        match Result[1]:
            case '__Description__':
                if Result[0].find('.') == -1: Temp_Tittle = f'{Result[0]}: {Result[2]}'
                else: Temp_Tittle = f'\t{Result[0]}: {Result[2]}'
                Temp_Tittle = Temp_Tittle.replace('.', ' ')
                EndList.append(Temp_Tittle)
            case 'Required':
                if Result[0][0] == '<':
                    Temp_Command = Result[0][Result[0].find('.')+1:].replace('.', ' ')
                else:
                    Temp_Command = Result[0].replace('.', ' ')
                for Value in Result[2]: Temp_Command += f' {Value}'
                if Result[0].find('.') == -1: Temp_Command = f'\tCommand: {Temp_Command}\n'
                else: Temp_Command = f'\t\tCommand: {Temp_Command}\n'
                EndList.append(Temp_Command)
    return EndList

def VerifyCommand(Commands: ConfigEditor, Command: list, CaseSensitive: bool):
    """对 Command 执行完整校验流程, 并确保校验通过的 Command 为标准格式.

    Args:
        Commands (ConfigEditor): _预设指令集._
        Command (list): _用户键入的指令._
        CaseSensitive (bool): _是否区分大小写._

    Returns:
        (list[str] | bool[False]): _[变量_1, 变量_2, ...], 校验失败返回 False_
    """
    def CaseCorrection(Commands: ConfigEditor, Command: list, CaseSensitive: bool):
        """对 Command 进行大小写矫正, 在关键字相同(不区分大小写)的情况下, 将 Command 格式化为标准关键字.

        Args:
            Commands (ConfigEditor): _预设指令集._
            Command (list): _用户键入的指令._
            CaseSensitive (bool): _是否区分大小写._

        Raises:
            KeyError: _不匹配的关键字._

        Returns:
            _type_: _description_
        """
        try:
            KeyWords: tuple = Commands.Get_Keys('')
            for Index, KeyWord in enumerate(Command):
                if not 'Required' in KeyWords:
                    KeyWords = DualCaseSet(KeyWords)
                    Command[Index] = KeyWords.isIn(item=Command[Index], CaseSensitive=CaseSensitive)
                    if not Command[Index]:
                        raise KeyError(f'KeyError in Command Index {Index}.')
                else:
                    rsi = Index
                    Required = Commands.Get_Value(f'{Key_Locate}.Required')
                    CommandRule: list = Key_Locate.split('.') + Required
                    break
                Key_Locate = Command[0] if Index == 0 else f'{Key_Locate}.{Command[Index]}'
                KeyWords: tuple = Commands.Get_Keys(Key_Locate)
            zRequired = []
            for Index, KeyWord in enumerate(Required):
                if '(Optional)' in KeyWord: zRequired.append(Required[Index][:-10])
                else: zRequired.append(Required[Index])
            Required = zRequired
            Required = DualCaseSet(Required)
            for Index, KeyWord in enumerate(Command[rsi:]):
                if KeyWord[0] == '-':
                    Command[rsi+Index] = Required.isIn(item=Command[Index+1], CaseSensitive=CaseSensitive)
                    if not Command[Index+1]: raise KeyError(f'KeyError in Command Index {Index+1}.')
                elif KeyWord[0] == '<' and KeyWord[-1] == '>':
                    pass
                else:
                    raise KeyError(f'KeyError in Command Index {Index+1}.')
            return Command, CommandRule
        except:
            return False, False

    def ParseFormat(CommandRule: list):
        """将 CommandRule 解析成方便进行校验的格式.

        Args:
            FormatRule (str): _description_

        Returns:
            list[dict]: [{
                'optional': True | False\n
                'type': 'flag' | 'fixed' | 'var'\n
                'value': '<...> | -...'}]
        """
        Elements_Rule: list = []
        KeyWords: list = CommandRule
        Part_Variable = compile(r'^<([^>]+)>(\(Optional\))?$')
        Part_Flag = compile(r'^(-.+?)(\(Optional\))?$')
        for KeyWord in KeyWords:
            # Matching variable
            Match_Variable = Part_Variable.match(KeyWord)
            if Match_Variable:
                IsOptional: bool = Match_Variable.group(2) is not None
                Elements_Rule.append({'type': 'var', 'optional': IsOptional})
                continue
            # Matching Flag
            Match_Flag = Part_Flag.match(KeyWord)
            if Match_Flag:
                value = Match_Flag.group(1)
                IsOptional = Match_Flag.group(2) is not None
                Elements_Rule.append({'type': 'flag', 'value': value, 'optional': IsOptional})
                continue
            # Matching KeyWord
            Elements_Rule.append({'type': 'fixed', 'value': KeyWord, 'optional': False})
        return Elements_Rule

    def VerifyFormat(Command: list, CommandRule: list):
        """对 Command 进行全方位(类型, 格式, 符号)校验.

        Args:
            Command (list): _description_
            CommandRule (list): _description_
        Returns:
            _type_: _description_
        """
        if not Command or not CommandRule: return False
        Elements_Rule = ParseFormat(CommandRule)
        Elements_Input = Command
        R = I = 0
        while R < len(Elements_Rule) and I < len(Elements_Input):
            Current_Rule = Elements_Rule[R] # Take out a key word from the rule.
            Current_Input = Elements_Input[I] # Take out a key word from the input.
            match Current_Rule['type']:
                case 'fixed':
                    if Current_Input == Current_Rule['value']:
                        I += 1; R += 1
                    else: return False
                case 'var':
                    if Current_Input.startswith('<') and Current_Input.endswith('>'):
                        I += 1; R += 1
                    elif Current_Rule['optional']:
                        R += 1
                    else: return False
                case 'flag':
                    if Current_Input == Current_Rule['value']:
                        I += 1; R += 1
                    elif Current_Rule['optional']:
                        R += 1
                    else: return False
                case _:
                    return False
        while R < len(Elements_Rule):
            if not Elements_Rule[R]['optional']:
                return False
            R += 1
        if I != len(Elements_Input):
            return False
        args: list = [] # ['<Required_1>', '<Required_2>(Optional), -Flag_1, -Flag_2(Optional)']
        Index_Command: int = 0
        rsi: int = -1
        for Index, KeyWord in enumerate(CommandRule):
            if (KeyWord[0] in ['<', '-']) and (rsi==-1):
                rsi = Index
                Index_Command = Index
            if rsi == -1: continue

            if (not Index_Command > len(Command)-1) and (KeyWord[0] == Command[Index_Command][0]):
                args.append(Command[Index_Command])
                Index_Command += 1
            elif '(Optional)' in KeyWord:
                args.append('')
            else: return False
        return args

    return VerifyFormat(*CaseCorrection(Commands=Commands,
                                        Command=Command,
                                        CaseSensitive=CaseSensitive))

class CommandExecuter():
    def __init__(self,
                 PathCommands: str,
                 PathLanguage: str,
                 CaseSensitive: bool):
        self.Commands: ConfigEditor = self.__CommandLanMix(PathCommands=PathCommands, PathLanguage=PathLanguage)
        self.Methods: DualCaseSet = self.__GetMethods()
        self.CaseSensitive: str = CaseSensitive

        self.Initialize()

    def __GetMethods(self) -> DualCaseSet:
        zMethods = getmembers(self, predicate=ismethod)
        Methods: list = [zMethod[0] for zMethod in zMethods]
        for Name in ['Initialize', '_CommandExecuter__CommandLanMix', '_CommandExecuter__GetMethods', '__init__']:
            Methods.remove(Name)
        return DualCaseSet(Methods)
    
    def __CommandLanMix(self,
                        PathCommands: str,
                        PathLanguage: str) -> ConfigEditor:
        Commands: ConfigEditor = ConfigEditor(Data_Toml=ConfigEditor(Path_Toml=PathCommands).Get_Data_Toml())
        Language: ConfigEditor = ConfigEditor(Path_Toml=PathLanguage)
        Key_Locate: str = ''

        for Result in Language.Get_NestedPaths():
            Key_Locate = f'{Result[0]}.{Result[1]}'
            if Result[1] == '__Description__':
                Commands.Set_Value(Key_Locate=Key_Locate,
                                   Value=Language.Get_Value(Key_Locate))

        return Commands

    def Initialize(self):
        pass

    def Help(self, Command: list[str]) -> None:
        if not Command == ['Help']: ConsoleLog(f'Error Command -> {Command}'); return
        HelpList: list = CommandsToHelp(Commands=self.Commands,
                                        CommandsOrder=self.Commands.Get_Value('CommandsOrder'))

        for HelpLine in HelpList:
            print(f'\t{HelpLine}')

    def Clear(self, Command: list[str]) -> None:
        if not Command == ['Clear']: ConsoleLog(f'Error Command -> {Command}'); return
        from os import system
        system('cls')
    
    def Exit(self, Command: list[str]) -> None:
        if not Command == ['Exit']: ConsoleLog(f'Error Command -> {Command}'); return
        from sys import exit
        exit()

    def Example(self, Command: list[str]) -> None:
        Result: list | bool = VerifyCommand(Commands=self.Commands,
                                            Command=Command,
                                            CaseSensitive=self.CaseSensitive)
        if not Result: ConsoleLog(f'Error Command.'); return
        # 经过 VerifyCommand 校验后得到的 Result 是包含变量的列表, 只要按对应位置调用就行了.
        print(Result)

class CLI():
    """命令行的核心类, 用于创建命令等待循环, 指令处理部分交给 BasicCommandHandler 的子类.
    """
    def __init__(self,
                 PathCommands: str,
                 PathLanguage: str,
                 CLIName: str = 'Lucas CLI',
                 User: str = 'Steve',
                 CE: Type[CommandExecuter] = CommandExecuter,
                 CaseSensitive: bool = True
                 ):
        self.CLIName: str = CLIName
        self.User: str = User
        self.CE: CommandExecuter = CE(PathCommands=PathCommands,
                                      PathLanguage=PathLanguage,
                                      CaseSensitive=CaseSensitive)
        self.CaseSensitive: str = CaseSensitive
        
    def Start(self):
        self.Initialize()
        while 1:
            LoopPause(0.1)
            Command: str = input(f'User {self.User}>')
            self.CommandExecute(Command)

    def Initialize(self):
        print(ASCII_Art(Text=self.CLIName, AddSplit=True)[0])

    def CommandExecute(self, Command: str) -> None:
        VariableFlag: bool = False
        Indexs: list = [-1, -1]
        for Index, Char in enumerate(Command):
            if Char == '<':
                VariableFlag = True
                Indexs[0] = Index
            if Char == '>' and VariableFlag:
                VariableFlag = False
                Indexs[1] = Index
            if -1 not in Indexs:
                Command = Command[:Indexs[0]+1] + Command[Indexs[0]+1: Indexs[1]].replace(' ', '=') + Command[Indexs[1]:]
                Indexs = [-1, -1]

        Command: list = Command.split(' ')
        Command[0] = self.CE.Methods.isIn(item=Command[0], CaseSensitive=self.CaseSensitive)

        if Command[0]:
            getattr(self.CE, Command[0])(Command)
        else:
            ConsoleLog('Unknow Command.')
            return

def ExampleToml(Path_Toml: str = ''):
    Commands: str ='''CommandsOrder = [
    'Help',
    'Clear',
    'Exit',
    'Example'
]

[Help]
__Description__ = 'Used to demonstrate the usage method.'
Required = []

[Clear]
__Description__ = 'Used to clear the messages on the screen.'
Required = []

[Exit]
__Description__ = 'Used to Exit CLI.'
Required = []

# --------------------------------------------------

[Example]
__Description__ = 'A Example Method For CommandExecuter.'
Required = ['<Required_1>', '<Required_2>(Optional), -Flag_1, -Flag_2(Optional)']

# --------------------------------------------------'''
    zh_cn: str = '''[Help]
__Description__ = "用于演示使用方法。"
[Clear]
__Description__ = "用于清除屏幕上的消息。"
[Exit]
__Description__ = "用于退出CLI。"
[Example]
__Description__ = "CommandExecutor的一个示例方法。"'''
    if not Path_Toml: Path_Toml = '.'
    with open(file=fr'{Path_Toml}\Commands.toml', mode='w', encoding='utf-8') as File:
        File.write(Commands)
    with open(file=fr'{Path_Toml}\zh_cn.toml', mode='w', encoding='utf-8') as File:
        File.write(zh_cn)

def ExtractLang(Path_Toml: str, Path_Lang: str):
    Commands: ConfigEditor = ConfigEditor(Path_Toml=Path_Toml)
    CommandsOrder: tuple = Commands.Get_Value('CommandsOrder')
    Commands_Lang: ConfigEditor = ConfigEditor()
    TempList: list = []
    def DepthRecursion(Key_Locate: str):
        SubKeys_1: list = Commands.Get_Keys(Key_Locate=Key_Locate)
        for SubKey_1 in SubKeys_1:
            SubKey_Locate: str = f'{Key_Locate}.{SubKey_1}'
            SubKeys_2 = Commands.Get_Keys(Key_Locate=SubKey_Locate)
            if SubKeys_2: DepthRecursion(Key_Locate=SubKey_Locate)
            else: TempList.append([Key_Locate, SubKey_1, Commands.Get_Value(SubKey_Locate)])
    for Key in CommandsOrder: DepthRecursion(Key_Locate=Key)
    for Result in TempList:
        match Result[1]:
            case '__Description__':
                Commands_Lang.Set_Value(Key_Locate=f'{Result[0]}.{Result[1]}', Value=Result[2])
            case _: pass
    Commands_Lang.Save_Toml(FiledPath=Path_Lang)

if __name__ == '__main__':
    # Commands: ConfigEditor = ConfigEditor(Path_Toml=r'test\Class\CLI\Commands.toml')
    # Command: list = 'Example <Required_1> -Flag_1'.split(' ')
    # CaseSensitive = False
    # print(VerifyCommand(Commands=Commands,
    #                     Command=Command,
    #                     CaseSensitive=CaseSensitive))
    # --------------------------------------------------
    # _CLI_ = CLI(PathCommands=r'test\Class\CLI\Commands.toml',
    #             PathLanguage=r'test\Class\CLI\zh_cn.toml',
    #             CLIName='Lucas CLI',
    #             User='Lucas',
    #             CE=CommandExecuter,
    #             CaseSensitive=False)
    # _CLI_.Start()
    # --------------------------------------------------
    # ExampleToml()
    pass