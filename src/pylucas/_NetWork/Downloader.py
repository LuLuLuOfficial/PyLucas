import requests
from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Thread
from typing import Literal
from os.path import expanduser, exists
from platform import system
from pylucas import result
from hashlib import sha1, sha256, sha512
from time import time

def HashesVerify(HashMode: Literal['sha1', 'sha256', 'sha512'],
                 File: str,
                 FileHashes: dict):
    match HashMode:
        case 'sha1':
            Hash = sha1()
        case 'sha256':
            Hash = sha256()
        case 'sha512':
            Hash = sha512()
        case _:
            raise Exception('UnSupport Hash Mode.')
    with open(File, "rb") as f:
        for ByteBlock in iter(lambda: f.read(4096), b""):
            Hash.update(ByteBlock)
    if FileHashes[HashMode] == Hash.hexdigest():
        return True
    else:
        return False

class Progress():
    def __init__(self, downloaded: int, total_size: int):
        self.downloaded: int = downloaded
        self.total_size: int = total_size
        self.progress: str = f'{int(downloaded/total_size*10000)/100:.2f}%'

    def __repr__(self):
        return self.progress

    def __getitem__(self, index: Literal['progress', 'downloaded', 'total_size'] | int):
        if isinstance(index, int):
            return (self.progress, self.downloaded, self.total_size)[index]
        elif isinstance(index, str):
            return {"progress": self.progress, "downloaded": self.downloaded, "total_size": self.total_size}[index]

class Downloader(Thread):
    def __init__(self,
                 url: str,
                 FileName: str,
                 FileDir: Literal['Default'] = 'Default',
                 UseThreads: int = 2,
                 FileHashes: dict = {}):
        super().__init__()
        self.name = 'Thread-Downloade'
        self.daemon = True

        self.__Lock: Lock = Lock()
        self.__Progress: dict = {"downloaded": 0,
                                 "total_size": 1}
        self.__FileHashes: dict = FileHashes if any([(Key in FileHashes) for Key in FileHashes]) else {}
        self.__FileHashState: Literal[None, True, False] = None
        self.__DownloadState: Literal[None, True, False] = None
        self.TimeUse: float = 0

        self.url: str = url
        self.FileDir: str = self.DefaultDownloadDir() if FileDir == 'Default' else FileDir
        self.FileName: str = FileName
        self.FilePath: str = rf"{self.FileDir}\{FileName}"
        self.UseThreads: int = UseThreads

        self.FileCheck()
        self.start()

    def __bool__(self):
        return bool(self.__DownloadState)

    @property
    def Progress(self):
        with self.__Lock:
            zProgress: Progress = Progress(self.__Progress["downloaded"], self.__Progress["total_size"])
        return zProgress

    @property
    def FileVerify(self):
        return self.__FileHashState

    def FileCheck(self):
        if not exists(self.FileDir):
            raise FileNotFoundError(f'Folder <{self.FileDir}> Not Found, Make Sure The Dir Exist.')
        FileName: list = [self.FileName[:self.FileName.rfind('.')], self.FileName[self.FileName.rfind('.'):]]
        DupFileNum: int = 0
        
        while exists(self.FilePath):
            DupFileNum += 1
            self.FileName = f"{FileName[0]} ({DupFileNum}) {FileName[1]}"
            self.FilePath = rf"{self.FileDir}\{self.FileName}"
        with open(file=self.FilePath, mode='wb+') as File:
            File.truncate(0)

    def DefaultDownloadDir(self):
        match system():
            case "Windows":
                return f"{expanduser('~')}\Downloads"
            case "Darwin":
                return result(False, 'UnSupport Platfrom.')
            case "Linux":
                return result(False, 'UnSupport Platfrom.')
            case _:
                return result(False, 'UnSupport Platfrom.')

    def run(self):
        self.TimeUse = time()
        super().run()

        zResponse = requests.head(self.url)
        FileSize = int(zResponse.headers['Content-Length'])

        with open(file=self.FilePath, mode='wb+') as File:
            File.truncate(FileSize)

        with self.__Lock:
            self.__Progress["total_size"] = FileSize

        ChunkSize = FileSize // self.UseThreads
        SubChunkSizeBasic: int = 10*8*1024
        SubChunkSize = SubChunkSizeBasic if ChunkSize >= SubChunkSizeBasic * 5 else ChunkSize
        with ThreadPoolExecutor(max_workers=self.UseThreads) as executor:
            futures = []
            for i in range(self.UseThreads):
                Start = i * ChunkSize
                End = Start + ChunkSize - 1 if i != self.UseThreads-1 else FileSize - 1
                futures.append(executor.submit(self.Download_Chunk, Start, End, SubChunkSize))
            for future in futures:
                future.result()
        
        self.TimeUse = f'{(time()-self.TimeUse):.4f}'
        if self.__FileHashes: self.__FileHashState = HashesVerify(HashMode=list(self.__FileHashes.keys())[0],
                                                                  File=self.FilePath,
                                                                  FileHashes=self.__FileHashes)
        self.__DownloadState = self.__FileHashState if self.__FileHashes else True

    def Download_Chunk(self, Start: int, End: int, SubChunkSize: int):
        ChunkDownloaded: int = 0

        headers = {'Range': f'bytes={Start}-{End}'}
        with requests.get(self.url, headers=headers, stream=True) as zResponse:
            zResponse.raise_for_status()
            with open(self.FilePath, 'r+b') as File:
                File.seek(Start)

                for SubChunk in zResponse.iter_content(chunk_size=SubChunkSize):
                    if not SubChunk:
                        continue
                    File.write(SubChunk)
                    ChunkDownloaded += len(SubChunk)
                    if ChunkDownloaded >= SubChunkSize:
                        with self.__Lock: self.__Progress["downloaded"] += ChunkDownloaded
                        ChunkDownloaded = 0

                with self.__Lock: self.__Progress["downloaded"] += ChunkDownloaded

if __name__ == '__main__':
    test = Downloader(url='https://cdn.modrinth.com/data/TQTTVgYE/versions/IRAR0lWa/fabric-carpet-25w05a-1.4.165%2Bv250130.jar',
                    FileName='fabric-carpet-25w05a-1.4.165%2Bv250130.jar',
                    FileDir='Default',
                    UseThreads=1,
                    FileHashes={"sha512": "73443ba8020652ae01bde0a194803cb0ddbde54f0f0f05fa40163aa7e4151dcedfe722cbf2463d99702628e1434c3dc4caf9a0cce799469f20e1ec26f13c49cb",
                                "sha1": "850de39c5e5c0090374963e526d02fc3e4380ce6"})

    from time import sleep

    dobreak = False
    while test.FileVerify == None:
        sleep(0.05)
        print(f'{test.Progress}')
    else:
        print(f'{test.Progress}')
        print(f'Time Total Use: {test.TimeUse}')
        print(f'File Hash State: {test.FileVerify}')
        dobreak = True
