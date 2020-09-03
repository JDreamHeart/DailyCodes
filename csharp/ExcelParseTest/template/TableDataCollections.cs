using System.Collections.Generic;

public class TemplateRow : TableRowData {
    // TemplateType m_TemplateArg;
    // public TemplateType TemplateArg {
    //     get{ return m_TemplateArg; }
    // }

    public System.Int64 Id;

    static TableData<TemplateRow> m_data;

    public static TableData<TemplateRow> TableData() {
        if (m_data == null) {
            m_data = new TableData<TemplateRow>("[{\"Id\":233}]");
        }
        return m_data;
    }

}
