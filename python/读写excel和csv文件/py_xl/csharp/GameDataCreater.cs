using System.Collections.Generic;

class GameDataCreater {
    public static ITableData Create(string name) {
        switch (name) {
            case "TestTable":
            return TestTable();
        }
    }

}