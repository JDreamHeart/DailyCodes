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
