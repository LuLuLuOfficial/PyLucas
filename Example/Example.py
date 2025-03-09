if __name__ == '__main__':
    from PyLucas.Class.LogManager import LogManager
    from PyLucas.Function.Function import Author_Lucas, GetTimeStamp

    LogManage: LogManager = LogManager(OutPutPath_Root=r'Example\Log')
    LogManage.LogOutput(Level='Test', LogMassage='Just For Test...')
    LogManage.SetMassageLF(True)
    for n in range(10): LogManage.LogOutput()

    print(Author_Lucas())
    print(GetTimeStamp())
