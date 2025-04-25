from typing import Literal

def Author_Lucas(Author: str = 'Nuhil Lucas') -> str:
    """
    Generate Ascii Art Characters, This Func Mark with Deprecated, Recommended to use -> ASCII_Art.

    Args:
        Author (str, optional): _description_. Defaults to 'Nuhil Lucas'.

    Returns:
        str: _description_. Ascii Art Characters
    """
    from art import text2art
    ASCIIArt_Str: str = text2art(text=Author, font='starwars')
    SplitLine: str = '-'*(ASCIIArt_Str.find('\n')) + '\n'
    ASCIIArt_Str: str = SplitLine + ASCIIArt_Str + SplitLine
    LineCount: int = ASCIIArt_Str.count('\n')
    return ASCIIArt_Str, LineCount

def ASCII_Art(Text: str,
              Font: Literal['univers', 'tarty8', 'tarty7', 'tarty1', 'block'] = 'starwars',
              AddSplit: bool = False) -> str:
    """
    Generate Ascii Art Characters

    Args:
        Text (str): _description_. Source String.
        Font (str, 'univers'): _description_. Set the font for generating Ascii Art.
        AddSplit (bool, False): _description_. Add a context split line

    Returns:
        str: _description_. Ascii Art Characters
    """
    from art import text2art
    ASCIIArt_Str: str = text2art(text=Text, font=Font); SplitLine: str = ''
    if AddSplit: SplitLine: str = '-'*(ASCIIArt_Str.find('\n')) + '\n'
    ASCIIArt_Str: str = SplitLine + ASCIIArt_Str + SplitLine
    LineCount: int = ASCIIArt_Str.count('\n')
    return ASCIIArt_Str, LineCount

def GetTimeStamp(Split: str = '-') -> str:
    """
    Use To Get TimeStamp

    Args:
        Split (str, '-'): _description_. Used to separate units of time.

    Returns:
        str: _description_. Return a timestamp accurate to the second.
    """
    from time import localtime, strftime
    Time_Local: str = localtime()
    Time_Formatted: str = strftime(f'%Y{Split}%m{Split}%d %H{Split}%M{Split}%S', Time_Local)
    return Time_Formatted

def Get_CurrentFrame_Info() -> tuple[str]:  # 获取当前帧信息
    """
    Gets the current code execution location

    Returns:
        tuple[str]: _description_. (Path_File, Name_Func, FuncLine_Def, FuncLine_Current)
    """
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
