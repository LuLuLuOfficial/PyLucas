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

def GetCurrentFrameInfo() -> tuple[str]:  # 获取当前帧信息
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

def lindex(List: list, Value: any) -> int:
    """_用于从左侧查找值索引, 类似 str.find, 如未找到则返回 -1._

    Args:
        List (list): _待查找的列表._
        Value (any): _待查找的值._

    Returns:
        int: _从列表左侧开始找到的第一个索引值._
    """
    if not Value in List: return -1
    Index = List.index(Value)
    return Index

def rindex(List: list, Value: any) -> int:
    """_用于从右侧查找值索引, 类似 str.rfind, 如未找到则返回 -1._

    Args:
        List (list): _待查找的列表._
        Value (any): _待查找的值._

    Returns:
        int: _从列表右侧开始找到的第一个索引值._
    """
    if not Value in List: return -1
    Index = len(List) - 1 - list(reversed(List)).index(Value)
    return Index