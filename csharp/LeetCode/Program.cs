using System;
using System.Collections.Generic;
using System.Text;

namespace LeetCode
{
    class Program
    {
        static void Main(string[] args)
        {
            Solution7 s = new Solution7();
            DateTime startTime = DateTime.Now;
            double ret = s.FindMedianSortedArrays(new int[]{}, new int[]{4, 5, 6, 8, 9});
            TimeSpan diffTime = DateTime.Now - startTime;
            Console.WriteLine("Result: [{0}];\nCoast Time: [{1}].", ret, diffTime.Milliseconds);
            // StringBuilder str = new StringBuilder();
            // for (int i = 0; i < ret.Count; i ++) {
            //     str.AppendJoin(',', ret[i]);
            //     str.Append("|");
            // }
            // Console.WriteLine("Result: [{0}].", str.ToString());
            Console.WriteLine("Result: {0}", ret);
            // Console.ReadLine();
        }
    }
}
