using System;
using System.Collections.Generic;

class TemplateRowX {

}

namespace ExcelParseTest
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("========= Start ========");
            Run();
            Console.WriteLine("========= End ========");
        }

        static void Run() {
            GameData gd = new GameData();
            Console.WriteLine(gd);
            var ret = gd.Find<TemplateRow>(233);
            var ret1 = gd.Find<TemplateRow>(233, "id");
            var ret2 = gd.Find<TemplateRowX>(2333);
            var ret3 = gd.FindAll<TemplateRow>(233);
            var ret4 = gd.FindAll<TemplateRow>(233, "key");
            Console.WriteLine("========= Ret ======== {0}, {1}, {2}, {3}, {4}", ret, ret1, ret2==null, ret3.Length, ret4.Length);
        }
    }
}
