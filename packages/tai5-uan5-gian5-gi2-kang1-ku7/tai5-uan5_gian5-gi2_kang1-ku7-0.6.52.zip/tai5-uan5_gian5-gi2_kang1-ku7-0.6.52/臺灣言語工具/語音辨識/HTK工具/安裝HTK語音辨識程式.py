# -*- coding: utf-8 -*-
from 臺灣言語工具.系統整合.安裝程式腳本 import 安裝程式腳本
from os import makedirs
from os.path import join, isdir


from 臺灣言語工具.系統整合.外部程式 import 外部程式


class 安裝HTK語音辨識程式(安裝程式腳本):

    @classmethod
    def 安裝htk(cls, htk安裝路徑=外部程式.目錄()):
        makedirs(htk安裝路徑, exist_ok=True)
        htk程式碼目錄 = cls.htk程式碼目錄(htk安裝路徑)
        if not isdir(htk程式碼目錄):
            with cls._換目錄(htk安裝路徑):
                cls._走指令([
                    'git', 'clone',
                    '--branch', 'HTK3.5',
                    '--single-branch',
                    'https://github.com/a8568730/HTK_HTS.git',
                    'HTK',
                ])
        else:
            with cls._換目錄(htk程式碼目錄):
                cls._更新專案()
        with cls._換目錄(join(htk程式碼目錄, 'HTKLib')):
            cls._走指令(['make', '-f', 'MakefileCPU', 'all', 'install'])
        with cls._換目錄(join(htk程式碼目錄, 'HTKTools')):
            cls._走指令(['make', '-f', 'MakefileCPU', 'all', 'install'])

    @classmethod
    def htk程式碼目錄(cls, htk安裝路徑=外部程式.目錄()):
        return join(htk安裝路徑, 'HTK')

    @classmethod
    def htk執行檔目錄(cls, htk安裝路徑=外部程式.目錄()):
        return join(cls.htk程式碼目錄(htk安裝路徑), 'bin.cpu')
