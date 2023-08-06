# -*- coding: utf-8 -*-
from os import makedirs
from os.path import join, isdir


from 臺灣言語工具.語音辨識.HTK工具.安裝HTK語音辨識程式 import 安裝HTK語音辨識程式
from 臺灣言語工具.系統整合.外部程式 import 外部程式


class 安裝HTS語音辨識程式(安裝HTK語音辨識程式):

    @classmethod
    def sptk執行檔目錄(cls, sptk安裝路徑=外部程式.目錄()):
        return join(cls._sptk安裝目錄(sptk安裝路徑), 'bin')

    @classmethod
    def _sptk安裝目錄(cls, sptk安裝路徑=外部程式.目錄()):
        return join(sptk安裝路徑, 'SPTK', 'compiled')

    @classmethod
    def hts執行檔目錄(cls, 安裝路徑=外部程式.目錄()):
        return join(安裝路徑, 'HTS', 'bin')

    @classmethod
    def htsDemo目錄(cls, 安裝路徑=外部程式.目錄()):
        return join(安裝路徑, 'HTS-demo')

    @classmethod
    def 安裝sptk(cls, sptk安裝路徑=外部程式.目錄()):
        makedirs(sptk安裝路徑, exist_ok=True)
        sptk程式碼目錄 = join(sptk安裝路徑, 'SPTK')

        if not isdir(sptk程式碼目錄):
            with cls._換目錄(sptk安裝路徑):
                cls._走指令([
                    'git', 'clone',
                    'git://git.code.sf.net/p/sp-tk/SPTK',
                ])
        else:
            with cls._換目錄(sptk程式碼目錄):
                cls._更新專案()

        with cls._換目錄(join(sptk程式碼目錄, 'src')):
            with open('ChangeLog', 'w') as ChangeLog:
                cls._走指令(['git', 'log'], stdout=ChangeLog)
            cls._走指令(['aclocal'], 愛直接顯示輸出=True)
            cls._走指令(['autoconf'], 愛直接顯示輸出=True)
            cls._走指令(['automake', '--add-missing'], 愛直接顯示輸出=True)
            cls._走指令([
                './configure',
                '--prefix={}'.format(cls._sptk安裝目錄(sptk安裝路徑))
            ], 愛直接顯示輸出=True)
            cls._走指令(['make', 'all', 'install'], 愛直接顯示輸出=True)

    @classmethod
    def 安裝hts(cls, hts安裝路徑=外部程式.目錄()):
        makedirs(hts安裝路徑, exist_ok=True)
        hts程式碼目錄 = join(hts安裝路徑, 'HTS')
        if not isdir(hts程式碼目錄):
            with cls._換目錄(hts安裝路徑):
                cls._走指令([
                    'git', 'clone',
                    '--branch', 'hts',
                    '--single-branch',
                    'https://github.com/a8568730/HTK_HTS.git',
                    'HTS',
                ])
        else:
            with cls._換目錄(hts程式碼目錄):
                cls._更新專案()
        with cls._換目錄(hts程式碼目錄):
            try:
                cls._走指令(['make', 'all', 'install'])
            except OSError:
                cls._走指令(['chmod', 'u+x', 'configure'])
                cls._走指令([
                    './configure',
                    '--prefix={}'.format(hts程式碼目錄)
                ], 愛直接顯示輸出=True)
                cls._走指令(['make', 'all', 'install'], 愛直接顯示輸出=True)

    @classmethod
    def 掠htsDemoScript(cls, hts安裝路徑=外部程式.目錄()):
        makedirs(hts安裝路徑, exist_ok=True)
        htsDemo目錄 = cls.htsDemo目錄()
        if not isdir(htsDemo目錄):
            with cls._換目錄(hts安裝路徑):
                cls._走指令([
                    'git', 'clone',
                    '--single-branch',
                    'https://github.com/sih4sing5hong5/gi2_im1_moo5_hing5.git',
                    'HTS-demo',
                ])
        else:
            with cls._換目錄(htsDemo目錄):
                cls._更新專案()
