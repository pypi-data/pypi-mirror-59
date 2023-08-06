# -*- coding: utf-8 -*-
from os.path import join, isfile
from subprocess import Popen


from 臺灣言語工具.系統整合.外部程式 import 外部程式
from 臺灣言語工具.翻譯.摩西工具.安裝摩西翻譯佮相關程式 import 安裝摩西翻譯佮相關程式


class 摩西服務端():

    def __init__(self,
                 moses模型資料夾路徑,
                 埠='8080',
                 moses安裝路徑=外部程式.目錄(),
                 ):
        self.git執行程式 = join(
            安裝摩西翻譯佮相關程式.moses程式碼目錄(moses安裝路徑),
            'bin', 'mosesserver'
        )
        self.孤檔執行程式 = join(
            moses安裝路徑, 'mosesserver'
        )
        if isfile(self.git執行程式):
            self.執行程式 = self.git執行程式
        elif isfile(self.孤檔執行程式):
            self.執行程式 = self.孤檔執行程式
        else:
            raise OSError('{}抑是{}程式攏無存在！！'.format(
                self.git執行程式, self.孤檔執行程式
            ))
        self.模型路徑 = join(moses模型資料夾路徑, 'model', 'moses.ini')
        if not isfile(self.模型路徑):
            raise OSError('{0}模型無存在！！'.format(self.模型路徑))
        self.埠 = 埠
        self.程序 = None

    def 走(self):
        if not self.程序:
            self.程序 = Popen(
                [self.執行程式, '-f', self.模型路徑, '--server-port', str(self.埠)],
            )

    def 狀態(self):
        return self.程序.poll()

    def 等(self):
        return self.程序.wait()

    def 停(self):
        self.程序.terminate()
        self.程序 = None
