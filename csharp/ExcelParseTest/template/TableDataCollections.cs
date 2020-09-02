using System.Collections.Generic;

public class TemplateRow : TableRowData {
    // TemplateType m_TemplateArg;
    // public TemplateType TemplateArg {
    //     get{ return m_TemplateArg; }
    // }
}

public class TableDataCollectionsCreater : TableDataCreater {
    public TableDataCollectionsCreater() {
        m_typeDict.Add("TemplateName", TemplateRow,GetType());
        m_argsDict.Add("TemplateName", new object[,]{
            {},
        });
    }
}
