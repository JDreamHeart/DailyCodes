using System;
using System.Collections.Generic;
using System.Text;

namespace LeetCode
{
    class Program
    {
        static void Main(string[] args)
        {
            Solution6 s = new Solution6();
            DateTime startTime = DateTime.Now;
            IList<IList<int>> ret = s.ThreeSum(new int[]{-2, 0, 0, 2, 2});
            TimeSpan diffTime = DateTime.Now - startTime;
            Console.WriteLine("Result: [{0}];\nCoast Time: [{1}].", ret, diffTime.Milliseconds);
            StringBuilder str = new StringBuilder();
            for (int i = 0; i < ret.Count; i ++) {
                str.AppendJoin(',', ret[i]);
                str.Append("|");
            }
            Console.WriteLine("Result: [{0}].", str.ToString());
            // Console.ReadLine();
        }
    }
}
