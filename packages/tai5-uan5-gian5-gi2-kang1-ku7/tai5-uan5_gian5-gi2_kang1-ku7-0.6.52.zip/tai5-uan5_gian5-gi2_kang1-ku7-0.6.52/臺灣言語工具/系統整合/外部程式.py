# -*- coding: utf-8 -*-
import os


class 外部程式:
    @classmethod
    def 目錄(cls):
        程式所在 = os.path.abspath(__file__)
        while os.path.basename(程式所在) != '臺灣言語工具':
            程式所在 = os.path.dirname(程式所在)
        程式所在 = os.path.dirname(程式所在)
        return os.path.join(程式所在, '外部程式')
