﻿using System;
using System.Collections.Generic;
using System.Text;

namespace LeetCode
{
    class Program
    {
        static void Main(string[] args)
        {
            Solution3 s = new Solution3();
            DateTime startTime = DateTime.Now;
            IList<IList<int>> ret = s.ThreeSum(new int[]{0, 0, 0, 0});
            TimeSpan diffTime = DateTime.Now - startTime;
            Console.WriteLine("Result: [{0}];\nCoast Time: [{1}].", ret, diffTime.Milliseconds);
            foreach (IList<int> l in ret) {
                StringBuilder str = new StringBuilder();
                str.AppendJoin(',', l);
                Console.WriteLine("Result: [{0}].", str.ToString());
            }
            Console.ReadLine();
        }
    }
}
