using System;
using System.Reflection;
using System.Collections.Generic;

public class TableRowData {
    public void Init(object[] args, string[] keyList) {
        for (int i = 0; i < keyList.Length; i++) {
            if (i >= args.Length) {
                break;
            }
            string key = keyList[i];
            FieldInfo field = GetType().GetField(key);
            if (field == null) {
                continue;
            }
            field.SetValue(this, args[i]);
        }
    }

    public object this[string name]{
        get{
            FieldInfo fieldInfo = GetType().GetField(name);
            if (fieldInfo == null) {
                return null;
            }
			return fieldInfo.GetValue(this);
		}
    }
    
}

public class TableData<T> where T:TableRowData {
    Dictionary<string, Dictionary<object, List<int>>> m_dataMap = new Dictionary<string, Dictionary<object, List<int>>>();

    List<T> m_data = new List<T>();

    string m_defaultKey = "id";
    string[] m_keyList = new string[0];
    string[] m_exportKeyList = new string[0];

    public string DefaultKey {
        get { return m_defaultKey; }
    }

    public TableData(string keyJson, string exportKeyJson, string valJson) {
        initKey(keyJson, exportKeyJson);
        initVal(valJson);
    }

    void initKey(string keyJson, string exportKeyJson) {
        // 解析key列表
        List<object> keyList = MiniJSON.Json.Deserialize(keyJson) as List<object>;
        if (keyList != null) {
            m_keyList = new string[keyList.Count];
            keyList.CopyTo(m_keyList);
        }
        // 解析导出的key列表
        List<object> exportKeyList = MiniJSON.Json.Deserialize(exportKeyJson) as List<object>;
        if (exportKeyList != null) {
            m_exportKeyList = new string[exportKeyList.Count];
            exportKeyList.CopyTo(m_exportKeyList);
        }
        // 设置默认key值
        if (m_exportKeyList.Length > 0) {
            m_defaultKey = m_exportKeyList[0];
        } else if (m_keyList.Length > 0) {
            m_defaultKey = m_keyList[0];
        }
    }

    void initVal(string valJson) {
        List<object> valList = MiniJSON.Json.Deserialize(valJson) as List<object>;
        foreach (List<object> val in valList) {
            T data = Activator.CreateInstance<T>();
            data.Init(val.ToArray(), m_keyList);
            m_data.Add(data);
            // 加入到dataMap
            addToDataMap(data, m_data.Count - 1);
        }
    }

    void addToDataMap(T data, int index) {
        foreach (string exportKey in m_exportKeyList) {
            if (!m_dataMap.ContainsKey(exportKey)) {
                m_dataMap[exportKey] = new Dictionary<object, List<int>>();
            }
            object val = data[exportKey];
            if (val == null) {
                continue;
            }
            if (!m_dataMap[exportKey].ContainsKey(val)) {
                m_dataMap[exportKey][val] = new List<int>();
            }
            m_dataMap[exportKey][val].Add(index);
        }
    }

    object verifyType(object val) {
        Type valType = val.GetType();
        if (valType == typeof(Int16) || valType == typeof(Int32)) {
            return Int64.Parse(val.ToString());
        }
        return val;
    }

    // 根据导出的Key值获取【速度较快】
    public T Get(object val, string key) {
        if (m_dataMap.ContainsKey(key)) {
            val = verifyType(val);  // 校验类型
            if (m_dataMap[key].ContainsKey(val)) {
                List<int> indexList = m_dataMap[key][val];
                if (indexList.Count > 0) {
                    return m_data[indexList[0]];
                }
            }
        }
        return null;
    }
    public T[] GetAll(object val, string key) {
        List<T> rowList = new List<T>();
        if (m_dataMap.ContainsKey(key)) {
            val = verifyType(val);  // 校验类型
            if (m_dataMap[key].ContainsKey(val)) {
                List<int> indexList = m_dataMap[key][val];
                if (indexList.Count > 0) {
                    foreach (int i in indexList) {
                        rowList.Add(m_data[indexList[i]]);
                    }
                }
            }
        }
        return rowList.ToArray();
    }
    
    // 在整个表的数据中查找【速度缓慢】
    public T Find(object val, string key) {
        T rowData = this.Get(val, key);
        if (rowData != null) {
            return rowData;
        }
        val = verifyType(val);  // 校验类型
        for (int i = 0; i < m_data.Count; i++) {
            if (m_data[i][key] == null) {
                break;
            }
            if (m_data[i][key] == val) {
                return m_data[i];
            }
        }
        return null;
    }
    public T[] FindAll(object val, string key) {
        T[] rowArray = this.GetAll(val, key);
        if (rowArray.Length > 0) {
            return rowArray;
        }
        List<T> rowList = new List<T>();
        val = verifyType(val);  // 校验类型
        for (int i = 0; i < m_data.Count; i++) {
            if (m_data[i][key] == null) {
                break;
            }
            if (m_data[i][key] == val) {
                rowList.Add(m_data[i]);
            }
        }
        return rowList.ToArray();
    }
}
