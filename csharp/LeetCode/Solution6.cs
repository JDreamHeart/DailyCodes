// 给你一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？请你找出所有满足条件且不重复的三元组。

// 注意：答案中不可以包含重复的三元组

// 示例：

// 给定数组 nums = [-1, 0, 1, 2, -1, -4]，

// 满足要求的三元组集合为：
// [
//   [-1, 0, 1],
//   [-1, -1, 2]
// ]

using System;
using System.Collections;
using System.Collections.Generic;


namespace LeetCode {
    public class Solution6 {
        public IList<IList<int>> ThreeSum(int[] nums) {
            List<IList<int>> ret = new List<IList<int>>{};
            if (nums.Length < 3) {
                return ret;
            }
            Array.Sort(nums);
            if (nums[0] > 0 || nums[nums.Length - 1] < 0) {
                return ret;
            }
            for (int i = 0; i < nums.Length - 2; i ++) {
                if (nums[i] > 0) {
                    break;
                }
                if (i > 0 && nums[i] == nums[i-1]) {
                    continue;
                }
                int j = i + 1, k = nums.Length - 1;
                while(j < k) {
                    if (nums[k] < 0) {
                        break;
                    }
                    if (nums[i] + nums[j] + nums[k] < 0) {
                        j++;
                        continue;
                    } else if (nums[i] + nums[j] + nums[k] > 0) {
                        k--;
                        continue;
                    } else {
                        ret.Add(new int[3]{nums[i], nums[j], nums[k]});
                        while (++j < k) {
                            if (nums[j] != nums[j-1]) {
                                break;
                            }
                        }
                        while (j < --k) {
                            if (nums[k] != nums[k+1]) {
                                break;
                            }
                        }
                    }
                }
            }
            return ret;
        }
    }
}