using System;

namespace LeetCode
{
    class Program
    {
        static void Main(string[] args)
        {
            Solution s = new Solution();
            DateTime startTime = DateTime.Now;
            bool ret = s.IsMatch("", "c*");
            TimeSpan diffTime = DateTime.Now - startTime;
            Console.WriteLine("Result: [{0}];\nCoast Time: [{1}].", ret, diffTime.Milliseconds);
            Console.ReadLine();
        }
    }
}
