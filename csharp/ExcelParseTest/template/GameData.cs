using System.Reflection;
using System.Collections.Generic;

class GameData {
    Dictionary<string, TableData<TableRowData>> m_dataDict = new Dictionary<string, TableData<TableRowData>>();

    TableDataCreater m_dataCreater = new TableDataCreater();

    public TableData<TableRowData> this[string name] {
        get {
            if (!this.m_dataDict.ContainsKey(name)) {
                System.Type dataType = m_dataCreater.GetTypeByName(name);
                if (dataType == null) {
                    return null;
                }
                this.m_dataDict.Add(name, new TableData<dataType>());
            }
            return this.m_dataDict[name];
        }
    }
}

public class TableDataCreater {
    protected Dictionary<string, System.Type> m_typeDict = new Dictionary<string, System.Type>();

    protected Dictionary<string, object[,]> m_argsDict = new Dictionary<string, object[,]>();

    public System.Type GetTypeByName(string name) {
        if (m_typeDict.ContainsKey(name)) {
            return m_typeDict[name];
        }
        return null;
    }
    
    public object[,] GetArgsByName(string name) {
        if (m_argsDict.ContainsKey(name)) {
            return m_argsDict[name];
        }
        return null;
    }
}