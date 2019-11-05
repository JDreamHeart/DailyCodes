using System;
using System.Collections.Generic;
using System.Text;

namespace LeetCode
{
    class Program
    {
        static void Main(string[] args)
        {
            Solution4 s = new Solution4();
            DateTime startTime = DateTime.Now;
            IList<string> ret = s.LetterCombinations("23");
            TimeSpan diffTime = DateTime.Now - startTime;
            Console.WriteLine("Result: [{0}];\nCoast Time: [{1}].", ret, diffTime.Milliseconds);
            StringBuilder str = new StringBuilder();
            str.AppendJoin(',', ret);
            Console.WriteLine("Result: [{0}].", str.ToString());
            Console.ReadLine();
        }
    }
}
