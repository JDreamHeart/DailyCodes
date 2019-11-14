// 给定一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？找出所有满足条件且不重复的三元组。

// 注意：答案中不可以包含重复的三元组。

// 例如, 给定数组 nums = [-1, 0, 1, 2, -1, -4]，

// 满足要求的三元组集合为：
// [
//   [-1, 0, 1],
//   [-1, -1, 2]
// ]

using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;

namespace LeetCode{
    public class Solution3 {
        private Hashtable ht0 = new Hashtable();
        private Hashtable ht1 = new Hashtable();
        private Hashtable ht2 = new Hashtable();
        public IList<IList<int>> ThreeSum(int[] nums) {
            Array.Sort(nums);
            List<IList<int>> ret = new List<IList<int>>();
            List<int> lastList = new List<int>();
            for (int i = 0; i < nums.Length; i ++) {
                if (lastList.Count > 0 && lastList[0] == nums[i]) {
                    continue;
                }
                if (nums[i] > 0) {
                    break;
                }
                for (int j = i + 1; j < nums.Length; j ++) {
                    if (lastList.Count > 0 && lastList[0] == nums[i] && lastList[1] == nums[j]) {
                        continue;
                    }
                    if (nums[i] + nums[j] > 0) {
                        break;
                    }
                    // 查找对应的值
                    int k = Array.LastIndexOf(nums, - nums[i] - nums[j]);
                    if (k > j) {
                        lastList = new List<int>(){nums[i], nums[j], nums[k]};
                        ret.Add(lastList);
                    }
                }
            }
            return ret;
        }

        private string getMappingVal(params int[] nums) {
            StringBuilder str = new StringBuilder();
            foreach (int n in nums) {
                str.Append(n);
            }
            return str.ToString();
        }
    }
}