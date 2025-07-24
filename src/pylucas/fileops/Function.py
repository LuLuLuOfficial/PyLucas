from typing import Literal

def ListFiles(Root: str,
              Types: str | tuple = ('*',),
              Includes: str | tuple = '',
              Mode: Literal['Path', 'Name'] = 'Path') -> list[str]:
    from pathlib import Path
    """_summary_

    Args:
        Root (str): _description_
        Types (Union[str, tuple]): _description_
        Includes (Union[str, tuple], optional): _description_. Defaults to ''.
        Mode (Literal['Path', 'Name'], optional): _description_. Defaults to 'Path'.

    Returns:
        list: _description_
    """
    Types: tuple = (Types,) if isinstance(Types, str) else Types
    Includes: tuple = (Includes,) if isinstance(Includes, str) else Includes
    FileRoot: Path = Path(Root)
    Result: list = []
    for Type in Types: Result += [File.name for File in FileRoot.glob(Type) if all([(Include in File.name) for Include in Includes])]
    if Mode == 'Path': Result = [rf'{Root}\{FileName}' for FileName in Result]
    return Result

def FilesCopyer(Source: str, Target: str, Mode: Literal['Tree', 'File']):
    from os.path import exists as FileExist
    from pathlib import Path
    from shutil import copyfile
    from re import compile
    def IsRepeated(FileName: str):
        if '.' in FileName:
            Match: list = compile(' \(\d+\)\.').findall(FileName)
            if Match:
                Match: str = Match[-1]
                FileName: list = [FileName[:FileName.rfind(Match)],
                                Match[2: -2],
                                FileName[FileName.rfind(Match)+len(Match)-1:],]
            else:
                FileName: list = [FileName[:FileName.rfind('.')],
                                  '',
                                  FileName[FileName.rfind('.'):],]
        else:
            Match: list = compile(' \(\d+\)$').findall(FileName)
            print(Match)
            if Match:
                Match: str = Match[-1]
                FileName: list = [FileName[:FileName.rfind(Match)],
                                  Match[2: -1],
                                  '',]
            else:
                FileName: list = [FileName,
                                  '',
                                  '',]
        return FileName
    if not FileExist(Source): raise Exception('Source File or Source Folder Not Exist')
    if Mode == 'File': pass
    elif Mode == 'Tree': Target = Target + Source[Source.rfind("\\"):]
    Path(Target).mkdir(parents=True, exist_ok=True)

    for FileName in ListFiles(Root=Source, Mode='Name'):
        TargetRootFiles: list = ListFiles(Root=Target, Mode='Name')
        FileNamePart: list = IsRepeated(FileName)
        FileName_Target: str = FileName
        while FileName_Target in TargetRootFiles:
            FileNamePart[1] = 1 if FileNamePart[1] == '' else int(FileNamePart[1])+1
            FileName_Target = f'{FileNamePart[0]} ({FileNamePart[1]}){FileNamePart[2]}'
        FilePath_Target = rf'{Target}\{FileName_Target}'
        FilePath_Source: str = rf'{Source}\{FileName}'
        
        copyfile(FilePath_Source, FilePath_Target)

def FilesClear(*Target: tuple, Mode: Literal['Tree', 'File']):
    from os.path import isfile, isdir
    from os import remove
    from shutil import rmtree
    NewTarget: list = []
    if Mode == 'File':
        for zTarget in Target:
            if isdir(zTarget): NewTarget += ListFiles(zTarget)
            else: NewTarget.append(zTarget)
    for zTarget in NewTarget:
        if isfile(zTarget):
            remove(zTarget)
            continue
        elif isdir(zTarget):
            rmtree(zTarget)
            continue
