import os;
import re;
import json;
import shutil;
import xlrd;

class SheetDataParser(object):
    DEFAULT_DATA_TYPE = "STRING";
    DATA_TYPE_DICT = {
        "STRING" : {"func": lambda s: str(s), "default": ""},
        "INT" : {"func": lambda s: int(s), "default": 0},
        "BOOL" : {"func": lambda s: bool(s), "default": False},
        "FLOAT" : {"func": lambda s: float(s), "default": 0},
    };

    def __init__(self, sheet):
        super(SheetDataParser, self).__init__();
        self.__sheet = sheet;
        self.__startIndex = -1;
        self.__keyDict = {};
        self.__typeDict = {};
        self.__exportIdxList = [];
        self.__defaultDict = {};

        self.initKeyIndex();
        
    @property
    def isValid(self):
        if not self.name:
            return False;
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
        
    @property
    def idxList(self):
        idxList = list(self.__keyDict.keys());
        idxList.sort();
        return idxList;

    @property
    def keyList(self):
        keyList = [];
        for idx in self.idxList:
            keyList.append(self.__keyDict[idx]);
        return keyList;
        
    @property
    def exportKeyList(self):
        exportKeyList = [];
        for idx in self.__exportIdxList:
            exportKeyList.append(self.__keyDict[idx]);
        return exportKeyList;
        
    @property
    def valList(self):
        valList = [];
        if not self.isValid:
            return valList;
        idxList = self.idxList;
        for i in range(self.__startIndex, self.sheet.nrows):
            row = self.sheet.row_values(i);
            if self.checkIsAnnotated(row):
                continue;
            val = [];
            for idx in idxList:
                key = self.__keyDict[idx];
                typeFunc = self.DATA_TYPE_DICT[self.getTypeByKey(key)]["func"];
                if not row[idx]:
                    val.append(self.getDefaultByKey(key));
                else:
                    val.append(typeFunc(row[idx]));
            valList.append(val);
        return valList;

    @staticmethod
    def checkIsAnnotated(row):
        if re.search(r"^#.*", str(row[0])):
            return True;
        return False;
    
    def getTypeByKey(self, key):
        return self.__typeDict.get(key, self.DEFAULT_DATA_TYPE);
    
    def getDefaultByKey(self, key):
        typeParams = self.DATA_TYPE_DICT[self.getTypeByKey(key)];
        defaultVal = typeParams["default"];
        if key in self.__defaultDict:
            try:
                defaultVal = typeParams["func"](self.__defaultDict[key]);
            except Exception:
                pass
        return defaultVal;
    
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
                    if not isinstance(val, str):
                        continue;
                    valStrip = val.strip();
                    if valStrip == "*":
                        if i not in exportIdxList:
                            exportIdxList.append(i);
                    elif valStrip:
                        self.__keyDict[i] = valStrip;
                        if not exportIdxList:
                            exportIdxList.append(i);
                if self.__keyDict:
                    for i in exportIdxList:
                        if i in self.__keyDict:
                            self.__exportIdxList.append(i);
                    self.__exportIdxList.sort();
            else:
                for i, key in self.__keyDict.items():
                    if not isinstance(row[i], str):
                        continue;
                    typeStrip = row[i].strip();
                    ret = re.search("([a-zA-Z]+)\((.*)\)", typeStrip);
                    if not ret:
                        typeStr = typeStrip.upper();
                        if typeStr in self.DATA_TYPE_DICT:
                            self.__typeDict[key] = typeStr;
                    else:
                        typeStr = ret.group(1).upper();
                        if typeStr in self.DATA_TYPE_DICT:
                            self.__typeDict[key] = typeStr;
                            self.__defaultDict[key] = ret.group(2);
                if self.__typeDict:
                    break;
        self.__startIndex = startIdx;
    
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


class TableDataParser(object):
    def __init__(self, filePath):
        super(TableDataParser, self).__init__();
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

    @property
    def sheets(self):
        return iter(self);

class GameDataParser(object):
    def __init__(self, dirPath, outputPath, templatePath):
        super(GameDataParser, self).__init__();
        self.__dirPath = dirPath;
        self.__outputPath = outputPath;
        self.__templatePath = templatePath;
        self.verifyOutputPath();
    
    def verifyOutputPath(self):
        if not os.path.exists(self.__outputPath):
            os.makedirs(self.__outputPath);
    
    def copyTemplate(self):
        if not os.path.exists(self.__templatePath):
            return;
        for name in os.listdir(self.__templatePath):
            fullPath = os.path.join(self.__templatePath, name);
            if os.path.isdir(fullPath):
                shutil.copytree(fullPath, self.__outputPath);
            elif os.path.isfile(fullPath):
                shutil.copy(fullPath, self.__outputPath);

    def parse(self):
        self.copyTemplate();
        if not os.path.exists(self.__dirPath):
            return;
        for root, _, files in os.walk(self.__dirPath):
            for fileName in files:
                fullPath = os.path.join(root, fileName);
                dataParser = TableDataParser(fullPath);
                if dataParser.isValid:
                    self.onParse(dataParser);

    def onParse(self, dataParser):
        pass;

class CsharpGameDataParser(GameDataParser):
    DATA_TYPE_CONFIG = {
        "STRING" : "string",
        "INT" : "Int64",
        "BOOL" : "bool",
        "FLOAT" : "double",
    };

    COLLECTIONS_FILE_PATH = "";

    def getProperty(self, keyType, key):
        return f"    public {self.DATA_TYPE_CONFIG[keyType]} {key};"

    def getTemplate(self, className, properties, keyJson, exportKeyJson, valJson):
        keyJson = keyJson.replace("\"", "\\\"");
        exportKeyJson = exportKeyJson.replace("\"", "\\\"");
        valJson = valJson.replace("\"", "\\\"");
        return f"""

public class {className} : TableRowData {{
{properties}

    static TableData<{className}> m_data;
    public static TableData<{className}> TableData() {{
        if (m_data == null) {{
            string keyJson = "{keyJson}";
            string exportKeyJson = "{exportKeyJson}";
            string valJson = "{valJson}";
            m_data = new TableData<{className}>(keyJson, exportKeyJson, valJson);
        }}
        return m_data;
    }}
}}

"""

    def onParse(self, dataParser):
        with open(self.COLLECTIONS_FILE_PATH, "a+") as f:
            for sheet in dataParser.sheets:
                if not sheet.isValid:
                    continue;
                properties = [];
                for key in sheet.keyList:
                    properties.append(self.getProperty(sheet.getTypeByKey(key), key));
                template = self.getTemplate(sheet.name, "\n".join(properties),
                    json.dumps(sheet.keyList), json.dumps(sheet.exportKeyList), json.dumps(sheet.valList));
                # 追加
                f.write(template);


    

if __name__ == "__main__":

    dirPath = os.getcwd();

    # dataParser = TableDataParser(os.path.join(dirPath, "export_test.xlsx"));
    # for sheet in dataParser.sheets:
    #     print("=========== sheet.keyList =========", json.dumps(sheet.keyList));
    #     print("=========== sheet.exportKeyList =========", sheet.exportKeyList);
    #     print("=========== sheet.valList =========", sheet.valList);

    # dirPath = os.path.join(dirPath);
    outputPath = os.path.join(dirPath, "test", "output");
    dataParser = CsharpGameDataParser(dirPath, outputPath, "E:\\private\\project\\DailyCodes\\csharp\\ExcelParseTest\\template");
    dataParser.COLLECTIONS_FILE_PATH = os.path.join(dirPath, "test", "output", "TableDataCollections.cs");
    dataParser.parse();
