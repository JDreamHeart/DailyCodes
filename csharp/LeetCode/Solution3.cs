using System;
using System.Collections;
using System.Collections.Generic;

namespace LeetCode{
    public class Solution3 {
        public IList<IList<int>> ThreeSum(int[] nums) {
            Array.Sort(nums);
            List<IList<int>> ret = new List<IList<int>>{};
            for (int i = 0; i < nums.Length; i ++) {
                if (nums[i] > 0) {
                    break;
                }
                if (ret.Exists(x=>x[0]==nums[i])) {
                    Console.WriteLine("Resultaaa: [{0}]; [{1}].", nums[i], i);
                    continue;
                }
                Console.WriteLine("Resultxxx: [{0}]; [{1}].", nums[i], i);
                for (int j = i + 1; j < nums.Length; j ++) {
                    if (nums[i] + nums[j] > 0) {
                        break;
                    }
                    for (int k = j + 1; k < nums.Length; k ++) {
                        if (nums[i] + nums[j] + nums[k] == 0) {
                            ret.Add(new List<int>(){nums[i], nums[j], nums[k]});
                        }
                    }
                }
            }
            return ret;
        }
    }
}