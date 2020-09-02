using System.Collections.Generic;

class GameData {
    Dictionary<string, TableData> m_dataDict = new Dictionary<string, TableData>();

    GameData m_instance;

    public static GameData Instance() {
        if (m_instance != null) {
            return m_instance;
        }
        m_instance = GameData();
        return m_instance;
    }

    public TableData this[string name] {
        get {
            if (!this.m_dataDict.ContainsKey(name)) {
                this.m_dataDict.Add(name, GameDataCreater.Create(name));
            }
            return this.m_dataDict[name];
        }
    }

}