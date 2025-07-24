import win32gui
from pprint import pprint
import win32api
import win32con
from types import NoneType
from typing import Literal

def Open():
    path = r"D:\_PsPL\MediaPlayer\Text_Player\Notepad3\Notepad3.exe"
    hinst = win32api.ShellExecute(0, "", path, "", "", 1)
    print(hinst)

def GetWindows() -> list:
    Windows: list = []
    def callback(hwnd, hwnd_list):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            Windows.append([hwnd, title, class_name])
        return True  # 返回 True 继续枚举
    win32gui.EnumDesktopWindows(None, callback, None)
    return Windows

class Window():
    def __init__(self, hwnd: int) -> None:
        self.hwnd: int = hwnd

        if not self.IsExist: raise Exception('Non-Existent Window')

    @property
    def IsExist(self) -> bool:
        return bool(win32gui.IsWindow(self.hwnd))

    @property
    def WindowTitle(self) -> str:
        return win32gui.GetWindowText(self.hwnd)
    
    @property
    def WindowClassName(self) -> str:
        return win32gui.GetClassName(self.hwnd)
    
    def SetGeometry(self, x: int, y: int, width: int, height: int):
        win32gui.MoveWindow(self.hwnd, x, y, width, height, True)

    def SetForeground(self) -> None:
        win32gui.SetForegroundWindow(self.hwnd)

    def SetWindowHidden(self, Hide: bool | NoneType = None):
        match Hide:
            case True:
                win32gui.ShowWindow(self.hwnd, win32con.SW_HIDE)
            case False:
                win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
            case None:
                pass
        return None
    
    def SetWindowSize(self, Mode: Literal['MINIMIZE', 'MAXIMIZE'] | NoneType = None):
        match Mode:
            case 'MINIMIZE':
                win32gui.ShowWindow(self.hwnd, win32con.SW_MINIMIZE)
            case 'MAXIMIZE':
                win32gui.ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)
            case None:
                pass

def get_first_level_children(hwnd_parent):
    children = []
    win32gui.EnumChildWindows(hwnd_parent, lambda hwnd, result: result.append(hwnd), children)
    return children

from pprint import pprint
pprint(GetWindows())
