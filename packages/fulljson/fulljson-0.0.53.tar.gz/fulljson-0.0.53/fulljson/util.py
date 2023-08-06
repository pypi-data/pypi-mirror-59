# -*- coding: UTF-8 -*-

JSON_DELIMITER = ['{', '[', '"', ']', '}', ':', ',']

CLASS_OBJECT = type({})
CLASS_ARRAY = type([])
CLASS_TUPLE = type(())
CLASS_STRING = type('')
CLASS_FLOAT = type(1.0)
CLASS_INT = type(1)
CLASS_BOOL = type(True)
CLASS_NULL = type(None)

PRIMARY_CLASS4JSON = [CLASS_STRING, CLASS_FLOAT, CLASS_INT, CLASS_BOOL, CLASS_NULL]
COLLECTION_CLASS4JSON = [CLASS_OBJECT, CLASS_ARRAY, CLASS_TUPLE]

class JSONIllegalChar():
    def __init__(self, msg=None):
        self.msg = msg

    def __repr__(self):
        if self.msg == None:
            return 'Ukown json character'
        else:
            return self.msg

    def __str__(self):
        if self.msg == None:
            return 'Ukown json character'
        else:
            return self.msg

class JSONEmptyChar():
    def __init__(self):
        pass

    def __repr__(self):
        return 'Empty json character'

    def __str__(self):
        return 'Empty json character'

class JSONStrUtil:
    @staticmethod
    def isNumber(str):
        str = str.strip()
        if str == '':
            return False
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        point_num = 0
        for ch in str:
            if ch == '.':
                point_num = point_num + 1
            elif ch not in numbers:
                return False
        return point_num < 2

    @staticmethod
    def isInt(str):
        str = str.strip()
        if str == '':
            return False
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        point_num = 0
        for ch in str:
            if ch == '.':
                point_num = point_num + 1
            elif ch not in numbers:
                return False
        return point_num == 0

    @staticmethod
    def isFloat(str):
        str = str.strip()
        if str == '':
            return False
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        point_num = 0
        for ch in str:
            if ch == '.':
                point_num = point_num + 1
            elif ch not in numbers:
                return False
        return point_num == 1

    @staticmethod
    def isBool(str):
        str = str.strip()
        if str == '':
            return False
        return (str == 'true' or str == 'false')

    @staticmethod
    def isTrue(str):
        str = str.strip()
        if str == '':
            return False
        return str == 'true'

    @staticmethod
    def isFalse(str):
        str = str.strip()
        if str == '':
            return False
        return str == 'false'

    @staticmethod
    def isNull(str):
        str = str.strip()
        if str == '':
            return False
        return str == 'null'

    @staticmethod
    def isStr(str):
        # "ad"b" is not a string
        str = str.strip()
        if str == '' or len(str) < 2:
            return False
        if str[0] != '"' or str[-1] != '"':
            return False
        str = str[1:len(str)-1]
        if str.find('"') != -1:
            return False
        else:
            return True

    @staticmethod
    def valueOf(str):
        str = str.strip()
        obj = JSONEmptyChar()
        if str == '':
            return obj
        if JSONStrUtil.isNull(str):
            obj = None
        elif JSONStrUtil.isFloat(str):
            obj = float(str)
        elif JSONStrUtil.isInt(str):
            obj = int(str)
        elif JSONStrUtil.isBool(str):
            obj = bool(str)
        elif JSONStrUtil.isStr(str):
            obj = str[1:len(str)-1]
        else:
            obj = JSONIllegalChar()
        return obj

class KeyValue:
    def __init__(self, key, value, border=False):
        self.key = key
        self.value = value
        self.border = border

    def __repr__(self):
        return str(self.key) + ':' + str(self.value)

    def __str__(self):
        return str(self.key) + ':' + str(self.value)
    
    def isBorder(self):
        return self.border

class TypeValue:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return str(self.type) + ':' + str(self.value)

    def __str__(self):
        return str(self.type) + ':' + str(self.value)