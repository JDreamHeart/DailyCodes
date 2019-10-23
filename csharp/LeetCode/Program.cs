using System;

namespace LeetCode
{
    class Program
    {
        static void Main(string[] args)
        {
            Solution2 s = new Solution2();
            DateTime startTime = DateTime.Now;
            string ret = s.IntToRoman(1994);
            TimeSpan diffTime = DateTime.Now - startTime;
            Console.WriteLine("Result: [{0}];\nCoast Time: [{1}].", ret, diffTime.Milliseconds);
            Console.ReadLine();
        }
    }
}
