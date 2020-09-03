using System;
using System.Collections.Generic;

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
            var ret = gd.Find<TemplateRow>(233, "Id");
            Console.WriteLine("========= Ret ======== {0}", ret);
        }
    }
}
