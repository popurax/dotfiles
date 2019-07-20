#!/usr/bin/python3
import platform
import logging
from collections import defaultdict
import os
from os import path


messageFormat = "[%(who)s %(count)s回目] %(message)s"
formatter = logging.Formatter(messageFormat)
stdHandler = logging.StreamHandler()
stdHandler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[stdHandler])
class ExtensionLogRecord(logging.LogRecord):
        counts = defaultdict(int)
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            msg = str(self.msg)
            self.counts[msg] += 1
            self.who = platform.uname().node
            self.count = self.counts[msg]
logging.setLogRecordFactory(ExtensionLogRecord)
log = logging.getLogger(__name__)

ignoreFiles = [
    path.basename(__file__),
    ".git",
    ".vscode",
]

currentDir = path.dirname(path.abspath(__file__))

def main():
    pf = platform.system()
    if(pf == 'Windows'):
        pathProfile = os.environ["USERPROFILE"] + \
            "\Documents\WindowsPowerShell"
        files = [i for i in os.listdir(".") if not i in ignoreFiles]
        ps1s = [i for i in files if i.split(".")[-1] == "ps1"]
        # 戻り値が__NoneType__で例外処理とか増えていきそうなので、for句を使う。
        for i in ps1s:
            # 大半のWin環境はプロファイルディレクトリが無い。無ければ作る。
            if not path.isdir(pathProfile):
                os.mkdir(pathProfile)
            log.debug(currentDir)
            os.symlink(path.join(currentDir, i), path.join(pathProfile, i))
    elif(pf == 'Linux'):
        pathProfile = os.environ["HOME"]
        log.info(pf)
        files = [i for i in os.listdir(".") if not i in ignoreFiles]
        shellScripts = [i for i in files if not i.split(".")[-1] == "ps1"]
        for i in shellScripts:
            os.symlink(path.join(currentDir, i), path.join(pathProfile, i))
    else:
        pass


if __name__ == "__main__":
    main()
