# -*- coding: utf-8 -*-
from 臺灣言語工具.基本物件.公用變數 import 分字符號
from 臺灣言語工具.基本物件.公用變數 import 分詞符號
from 臺灣言語工具.解析整理.程式掠漏 import 程式掠漏


class 物件譀鏡:

    @classmethod
    def 看型(cls, 物件, 物件分字符號='', 物件分詞符號='', 物件分句符號=''):
        try:
            return 物件.看型(
                物件分字符號=物件分字符號,
                物件分詞符號=物件分詞符號,
                物件分句符號=物件分句符號,
            )
        except AttributeError:
            程式掠漏.毋是字詞組集句章的毋著(物件)

    @classmethod
    def 看音(cls, 物件, 物件分字符號=分字符號, 物件分詞符號=分詞符號, 物件分句符號=分詞符號):
        try:
            return 物件.看音(
                物件分字符號=物件分字符號,
                物件分詞符號=物件分詞符號,
                物件分句符號=物件分句符號,
            )
        except AttributeError:
            程式掠漏.毋是字詞組集句章的毋著(物件)

    @classmethod
    def 看分詞(cls, 物件):
        try:
            return 物件.看分詞()
        except AttributeError:
            程式掠漏.毋是字詞組集句章的毋著(物件)
