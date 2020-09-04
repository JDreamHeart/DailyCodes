using System;
using System.Reflection;
using System.Collections.Generic;

public class TableRowData {
    public void Init(Dictionary<string, object> arg) {
        FieldInfo[] fields = GetType().GetFields();
        for (int i = 0; i < fields.Length; i++) {
            string name = fields[i].Name;
            if (!arg.ContainsKey(name)) {
                continue;
            }
            fields[i].SetValue(this, arg[name]);
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
		set{
			// GetType().GetProperty(name).SetValue(this, value);
		}
    }
    
}

public class TableData<T> where T:TableRowData {
    Dictionary<string, Dictionary<object, int[]>> m_dataMap = new Dictionary<string, Dictionary<object, int[]>>();

    List<T> m_data = new List<T>();

    string m_defaultKey;

    public TableData(string defaultKey="id") {
        m_defaultKey = defaultKey;
    }

    public void Init(string jsonData) {
        List<object> args = MiniJSON.Json.Deserialize(jsonData) as List<object>;
        foreach (Dictionary<string, object> arg in args) {
            T data = Activator.CreateInstance<T>();
            data.Init(arg);
            m_data.Add(data);
        }
    }

    public string DefaultKey {
        get { return m_defaultKey; }
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
                int[] indexList = m_dataMap[key][val];
                if (indexList.Length > 0) {
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
                int[] indexList = m_dataMap[key][val];
                if (indexList.Length > 0) {
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
            if (m_data[i][key].Equals(val)) {
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
            if (m_data[i][key].Equals(val)) {
                rowList.Add(m_data[i]);
            }
        }
        return rowList.ToArray();
    }
}
