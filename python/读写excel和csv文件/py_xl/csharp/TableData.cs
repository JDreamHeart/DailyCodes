using System.Collections.Generic;

public class TableRowData {
    string id;

    public TableRowData(string id) {
        this.id = id;
    }

    public object this[string name]{
        get{
			return GetType().GetProperty(name).GetValue(this);
		}
		set{
			// GetType().GetField(name).SetValue(this,value);
		}
    }
}

public class TableData {
    Dictionary<string, Dictionary<string, int[]>> m_dataMap = new Dictionary<string, Dictionary<string, int[]>>();
    List<TableRowData> m_data = new List<TableRowData>();

    public TableData() {
        m_data.Add(TableRowData("0"));
        m_data.Add(TableRowData("1"));
        m_data.Add(TableRowData("2"));
    }

    // 根据导出的Key值获取【速度较快】
    public virtual TableRowData Get(string val, string key) {
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
    public virtual TableRowData[] GetAll(string val, string key) {
        List<TableRowData> rowList = new List<TableRowData>();
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
    public virtual TableRowData Find(string val, string key) {
        TableRowData rowData = this.Get(val, key);
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
    public virtual TableRowData[] FindAll(string val, string key) {
        TableRowData[] rowArray = this.Get(val, key);
        if (rowArray != null) {
            return rowArray;
        }
        List<TableRowData> rowList = new List<TableRowData>();
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
    public TableRowData Get(int id, string index) {
        return this.Get(id.ToString(), index);
    }
    public TableRowData[] GetAll(int id, string index) {
        return this.GetAll(id.ToString(), index);
    }

    public TableRowData Find(int id, string index) {
        return this.Find(id.ToString(), index);
    }
    public TableRowData[] FindAll(int id, string index) {
        return this.FindAll(id.ToString(), index);
    }
    
    // 查找bool类型
    public TableRowData Get(bool flag, string index) {
        return this.Get(Convert.ToInt32(flag), index);
    }
    public TableRowData[] GetAll(bool flag, string index) {
        return this.GetAll(Convert.ToInt32(flag), index);
    }

    public TableRowData Find(bool flag, string index) {
        return this.Find(Convert.ToInt32(flag), index);
    }
    public TableRowData[] FindAll(bool flag, string index) {
        return this.FindAll(Convert.ToInt32(flag), index);
    }
}
