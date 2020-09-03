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
			return GetType().GetField(name).GetValue(this);
		}
		set{
			// GetType().GetProperty(name).SetValue(this, value);
		}
    }
    
}

public class TableData<T> where T:TableRowData {
    Dictionary<string, Dictionary<object, int[]>> m_dataMap = new Dictionary<string, Dictionary<object, int[]>>();

    List<T> m_data = new List<T>();

    public TableData(string jsonData) {
        List<object> args = MiniJSON.Json.Deserialize(jsonData) as List<object>;
        // Dictionary<string, object> args = MiniJSON.Json.Deserialize(jsonData) as Dictionary<string, object>;
        foreach (Dictionary<string, object> arg in args) {
            T data = Activator.CreateInstance<T>();
            data.Init(arg);
            m_data.Add(data);
        }
    }

    // 根据导出的Key值获取【速度较快】
    public T Get(object val, string key) {
        if (m_dataMap.ContainsKey(key)) {
            if (m_dataMap[key].ContainsKey(val)) {
                int[] indexList = m_dataMap[key][val];
                if (indexList.Length > 0) {
                    return m_data[indexList[0]];
                }
            }
        }
        return default(T);
    }
    public T[] GetAll(object val, string key) {
        List<T> rowList = new List<T>();
        if (m_dataMap.ContainsKey(key)) {
            if (m_dataMap[key].ContainsKey(val)) {
                int[] indexList = m_dataMap[key][val];
                if (indexList.Length > 0) {
                    foreach (int i in indexList) {
                        rowList.Add(m_data[indexList[i]]);
                    }
                    return rowList.ToArray();
                }
            }
        }
        return null;
    }
    
    // 在整个表的数据中查找【速度缓慢】
    public T Find(object val, string key) {
        T rowData = this.Get(val, key);
        if (rowData != default(T)) {
            return rowData;
        }
        for (int i = 0; i < m_data.Count; i++) {
            Console.WriteLine("========= Find ======== {0}, {1}, {2}", m_data[i][key], val,  m_data[i][key].ToString() == val.ToString());
            if (m_data[i][key].Equals(val)) {
                return m_data[i];
            }
        }
        return null;
    }
    public T[] FindAll(object val, string key) {
        T rowArray = this.Get(val, key);
        if (rowArray != null) {
            return new T[]{rowArray};
        }
        List<T> rowList = new List<T>();
        for (int i = 0; i < m_data.Count; i++) {
            if (m_data[i][key].Equals(val)) {
                rowList.Add(m_data[i]);
            }
        }
        if (rowList.Count > 0) {
            return rowList.ToArray();
        }
        return null;
    }
}
