using System;

namespace ExcelParseTest
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("========= Start ========");
            this.Run();
            Console.WriteLine("========= End ========");
        }

        static void Run() {
            GameData gd = new GameData();
            Console.WriteLine(gd);
        }
    }
}
