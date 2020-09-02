using System;
using System.Reflection;
using System.Collections.Generic;

public class TableRowData {
    public TableRowData(params object[] args) {
        PropertyInfo[] properties = this.GetType().GetProperties();
        for (int i = 0; i < properties.Length; i++) {
            if (args.Length <= i) {
                break;
            }
            properties[i].SetValue(this, args[i]);
        }
    }

    public string this[string name]{
        get{
			return GetType().GetProperty(name).GetValue(this).ToString();
		}
		set{
			// GetType().GetProperty(name).SetValue(this, value);
		}
    }
}

public class TableData<T> where T:TableRowData {
    Dictionary<string, Dictionary<string, int[]>> m_dataMap = new Dictionary<string, Dictionary<string, int[]>>();

    List<T> m_data = new List<T>();

    public TableData(params object[] args) {
        foreach (object arg in args) {
            m_data.Add(Activator.CreateInstance(T, arg));
        }
    }

    // 根据导出的Key值获取【速度较快】
    public T Get(string val, string key) {
        if (m_dataMap.ContainsKey(key)) {
            if (m_dataMap[key].ContainsKey(val)) {
                int[] indexList = m_dataMap[key][val];
                if (indexList.Length > 0) {
                    return m_data[indexList[0]];
                }
            }
        }
        return null;
    }
    public T[] GetAll(string val, string key) {
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
    public T Find(string val, string key) {
        T rowData = this.Get(val, key);
        if (rowData != null) {
            return rowData;
        }
        for (int i = 0; i < m_data.Count; i++) {
            if ((string)m_data[i][key] == val) {
                return m_data[i];
            }
        }
        return null;
    }
    public T[] FindAll(string val, string key) {
        T[] rowArray = this.Get(val, key);
        if (rowArray != null) {
            return rowArray;
        }
        List<T> rowList = new List<T>();
        for (int i = 0; i < m_data.Count; i++) {
            if ((string)m_data[i][key] == val) {
                rowList.Add(m_data[i]);
            }
        }
        if (rowList.Count > 0) {
            return rowList.ToArray();
        }
        return null;
    }

    // 查找int类型
    public T Get(int id, string index) {
        return this.Get(id.ToString(), index);
    }
    public T[] GetAll(int id, string index) {
        return this.GetAll(id.ToString(), index);
    }

    public T Find(int id, string index) {
        return this.Find(id.ToString(), index);
    }
    public T[] FindAll(int id, string index) {
        return this.FindAll(id.ToString(), index);
    }
    
    // 查找bool类型
    public T Get(bool flag, string index) {
        return this.Get(flag.ToString(), index);
    }
    public T[] GetAll(bool flag, string index) {
        return this.GetAll(flag.ToString(), index);
    }

    public T Find(bool flag, string index) {
        return this.Find(flag.ToString(), index);
    }
    public T[] FindAll(bool flag, string index) {
        return this.FindAll(flag.ToString(), index);
    }
}
