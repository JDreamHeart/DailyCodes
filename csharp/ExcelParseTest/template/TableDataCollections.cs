using System;
using System.Collections.Generic;

public class TemplateRow : TableRowData {
    public Int64 id;

    static TableData<TemplateRow> m_data;
    public static TableData<TemplateRow> TableData() {
        if (m_data == null) {
            m_data = new TableData<TemplateRow>();
            m_data.Init("[{\"id\":233}]");
        }
        return m_data;
    }

}
