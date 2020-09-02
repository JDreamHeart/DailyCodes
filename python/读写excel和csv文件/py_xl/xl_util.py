import os;
import re;
import xlrd;

class SheetDataParser(object):
    DEFAULT_DATA_TYPE = "str";
    DATA_TYPE_LIST = {
        "int" : lambda s: int(s),
        "bool" : lambda s: bool(s),
        "str" : lambda s: str(s),
    };

	def __init__(self, sheet):
        super(SheetDataParser, self).__init__();
        self.__sheet = sheet;
        self.__iterIndex = -1;
        self.__startIndex = -1;
        self.__keyDict = {};
        self.__typeDict = {};
        self.__exportKeyList = [];

        self.initKeyIndex();
        
    @property
    def isValid(self):
        return self.__startIndex > 0;
    
    @property
    def sheet(self):
        return self.__sheet;
    
    @property
    def name(self):
        ret = re.search(r".*\(([_a-zA-Z]+)\)$", self.sheet.name)
        if ret:
            return ret.group(1);
        return ""
    
    def __iter__(self):
        self.__iterIndex = self.__startIndex;
        return self;
    
    def __next__(self):
        if self.isValid and 0 <= self.__iterIndex < self.sheet.nrows:
            row = self.sheet.row_values(self.__iterIndex);
            self.__iterIndex += 1;
            if self.checkIsAnnotated(row):
                return self.__next__();
            return row;
        else:
            raise StopIteration;
        
    def values(self):
        return iter(self);
    
    def initKeyIndex(self):
        startIdx = -1;
        exportIdxList = [];
        for idx in range(self.sheet.nrows):
            startIdx = idx + 1;
            row = self.sheet.row_values(idx);
            if self.checkIsAnnotated(row):
                continue;
            if not self.__keyDict:
                for i, val in enumerate(row):
                    valStrip = val.strip();
                    if valStrip == "*":
                        if i not in exportIdxList:
                            exportIdxList.append(i);
                    elif valStrip:
                        self.__keyDict[i] = valStrip;
                        if not exportIdxList:
                            exportIdxList.append(i);
                if self.__keyDict:
                    for i, key in self.__keyDict.items():
                        if i in exportIdxList:
                            self.__exportKeyList.append(key);
            else:
                isHasType, typeDict = False, {};
                for i, key in self.__keyDict.items():
                    typeStrip = row[i].strip();
                    if typeStrip in self.DATA_TYPE_LIST:
                        isHasType = True;
                    else:
                        typeStrip = self.DEFAULT_DATA_TYPE;
                    typeDict[key] = typeStrip;
                if isHasType:
                    self.__typeDict = typeDict;
                    break;
        if not self.__typeDict:
            for key in self.__keyDict.values():
                self.__typeDict[key] = self.DEFAULT_DATA_TYPE;
        self.__keyIndex = startIdx;
    
    def convertKeyDict(self):
        newKeyDict = {};
        for i, key in self.__keyDict.items():
            ret = re.search(r"^([_a-zA-Z]+)\+\d*$", key);
            if ret:
                if key not in newKeyDict:
                    newKeyDict[key] = [];
                newKeyDict[key].append(i);
            else:
                newKeyDict[key] = i;
        return newKeyDict;

    def checkIsAnnotated(row):
        if re.search(r"^#.*", row[0]):
            return True;
        return False;


class TableDataParser(object):
	def __init__(self, filePath):
        super(XlDataParser, self).__init__();
        self.__filePath = filePath;
        self.__workbook = None;
        self.__iterIndex = 0;

        self.initWorkbook();
    
    def initWorkbook(self):
        try:
            self.__workbook = xlrd.open_workbook(self.__filePath);
        except Exception as e:
            print(f"Failed to open workbook[{self.__filePath}]! Err-> {e}");

    @property
    def isValid(self):
        return self.__workbook is not None;

    @property
    def filePath(self):
        return self.__filePath;

    def __iter__(self):
        self.__iterIndex = 0;
        return self;
    
    def __next__(self):
        if self.isValid and 0 <= self.__iterIndex < self.__workbook.nsheets:
            sheetData = SheetDataParser(self.__workbook.sheet_by_index(self.__iterIndex));
            self.__iterIndex += 1;
            if not sheetData.isValid:
                return self.__next__();
            return sheetData;
        else:
            raise StopIteration;

    def sheets(self):
        return iter(self);
