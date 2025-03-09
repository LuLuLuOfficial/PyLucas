from PyLucas.Class.LogManager import LogManager

if __name__ == '__main__':
    LogManage = LogManager(OutPutPath_Root=r'Test\Log')
    for n in range(10):
        LogManage.LogOutput()