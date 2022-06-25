using System;
using System.Collections.Generic;

public class TemplateRow : TableRowData {
    public Int64 id;

    static TableData<TemplateRow> m_data;
    public static TableData<TemplateRow> TableData() {
        if (m_data == null) {
            string keyJson = "[\"id\"]";
            string exportKeyJson = "[\"id\"]";
            string valJson = "[[1001]]";
            m_data = new TableData<TemplateRow>(keyJson, exportKeyJson, valJson);
        }
        return m_data;
    }

}


public class TextTable : TableRowData {
    public Int64 id;
    public string key;
    public double val;
    public bool flag;

    static TableData<TextTable> m_data;
    public static TableData<TextTable> TableData() {
        if (m_data == null) {
            string keyJson = "[\"id\", \"key\", \"val\", \"flag\"]";
            string exportKeyJson = "[\"key\"]";
            string valJson = "[[1, \"you\", 0.3, false], [3, \"it\", 0, true]]";
            m_data = new TableData<TextTable>(keyJson, exportKeyJson, valJson);
        }
        return m_data;
    }
}

