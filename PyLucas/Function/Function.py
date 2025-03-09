def Author_Lucas(Author: str = 'Nuhil Lucas'):
    '''
    Generate ASCII Art.
    '''
    from pyfiglet import figlet_format
    Result = figlet_format(text=Author, font='starwars', direction='auto', justify='auto', width=10000)
    return Result

def GetTimeStamp(Split: str = '-'):
    '''
    Get Time Stamp.
    '''
    from time import localtime, strftime
    Time_Local: str = localtime()
    Time_Formatted: str = strftime(f'%Y{Split}%m{Split}%d %H{Split}%M{Split}%S', Time_Local)
    return Time_Formatted