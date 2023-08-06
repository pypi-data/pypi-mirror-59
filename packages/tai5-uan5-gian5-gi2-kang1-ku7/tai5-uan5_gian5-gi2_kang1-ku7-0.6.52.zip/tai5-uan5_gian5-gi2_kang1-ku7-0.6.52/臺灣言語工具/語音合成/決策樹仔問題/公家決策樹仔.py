# -*- coding: utf-8 -*-
from 臺灣言語工具.語音合成.生決策樹仔問題 import 生決策樹仔問題


class 公家決策樹仔:
    _生問題 = 生決策樹仔問題()

    @classmethod
    def 詞句長度(cls, 詞長, 句長):
        '''長度
        詞句 頭前中 長度 <=
        詞
                3*10*2
        句
                3*20*2
        '''
        詞 = []
        for 長度 in range(詞長 + 1):
            詞.append(('詞{}字'.format(長度),
                      ['{}'.format(長度)]))
        問題 = cls._生問題.問題集(詞, cls.詞符號, '連紲')
        句 = []
        for 長度 in range(句長 + 1):
            句.append(('句{}詞'.format(長度),
                      ['{}'.format(長度)]))
        問題 |= cls._生問題.問題集(句, cls.句符號, '連紲')
        恬的音 = [
            ('恬', ['x']),
        ]
        問題 |= cls._生問題.問題集(恬的音, cls.句符號, '孤條')
        return 問題

    @classmethod
    def 孤雙數音節(cls):
        return cls._生問題.問題集(
            [('孤數音節', ['*1', '*3', '*5', '*7', '*9'])],
            cls.句符號,
            '孤條'
        )
