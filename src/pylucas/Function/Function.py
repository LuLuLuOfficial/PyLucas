from typing import Literal

def Author_Lucas(Author: str = 'Nuhil Lucas'):
    '''
    Generate ASCII Art.
    Mark As Deprecated.
    '''
    from art import text2art
    Text_Format: str = text2art(text=Author, font='starwars')
    SplitLine: str = '-'*(Text_Format.find('\n')) + '\n'
    Result: str = SplitLine + Text_Format + SplitLine
    LineCount: int = Result.count('\n')
    return Result, LineCount

def ASCII_Art(Text: str, Font: Literal['univers', 'tarty8', 'tarty7', 'tarty1', 'block'] = 'univers'):
    '''
    Generate ASCII Art.
    '''
    from art import text2art
    Result = text2art(text=Text, font='starwars')
    return Result

def GetTimeStamp(Split: str = '-'):
    '''
    Get Time Stamp.
    '''
    from time import localtime, strftime
    Time_Local: str = localtime()
    Time_Formatted: str = strftime(f'%Y{Split}%m{Split}%d %H{Split}%M{Split}%S', Time_Local)
    return Time_Formatted

def Get_CurrentFrame_Info() -> tuple[str]:  # 获取当前帧信息
    '''
    return (Path_File, Name_Func, FuncLine_Def, FuncLine_Current)
    返回 (文件路径, 函数名, 函数定义的起始行号, 当前执行的行号)
    '''
    from inspect import currentframe
    # 获取当前栈帧
    CurrentFrame = currentframe()
    # 文件名
    Path_File: str = CurrentFrame.f_code.co_filename
    # 函数名
    Name_Func: str = CurrentFrame.f_code.co_name
    # 函数定义的起始行号
    FuncLine_Def: int = CurrentFrame.f_code.co_firstlineno
    # 当前执行的行号 - 即调用currentframe()的行
    FuncLine_Current: int = CurrentFrame.f_lineno
    return (Path_File, Name_Func, FuncLine_Def, FuncLine_Current)
