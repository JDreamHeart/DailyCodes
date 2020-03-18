// 给定两个大小为 m 和 n 的有序数组 nums1 和 nums2。

// 请你找出这两个有序数组的中位数，并且要求算法的时间复杂度为 O(log(m + n))。

// 你可以假设 nums1 和 nums2 不会同时为空。

// 示例 1:

// nums1 = [1, 3]
// nums2 = [2]

// 则中位数是 2.0
// 示例 2:

// nums1 = [1, 2]
// nums2 = [3, 4]

// 则中位数是 (2 + 3)/2 = 2.5


using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;


namespace LeetCode {
    public class Solution7 {
        // @return diff count
        void checkArrayMedian(int[] nums, int h, int r, int diff, out int hIdx, out int rIdx) {
            int median = (int)diff/2;
            hIdx = h + median;
            rIdx = r - median;
        }
        public double FindMedianSortedArrays(int[] nums1, int[] nums2) {
            int h1 = 0, h2 = 0, r1 = nums1.Length - 1, r2 = nums2.Length - 1;
            while(h1 <= r1 && h2 <= r2) {
                Console.WriteLine("h1: {0}, r1: {1}; h2: {2}, r2: {3}", h1, r1, h2, r2);
                // 判断剩余数
                if (h1 == r1 || h2 == r2) {
                    if (h1 == r1 && h2 == r2) {
                        return (double) (nums1[h1] + nums2[h2]) / 2;
                    } else if (h1 == r1) {
                        if (nums1[h1] > nums2[h2] && nums1[h1] < nums2[r2]) {
                            h2++;
                            r2--;
                        } else if (nums1[h1] <= nums2[h2]) {
                            h1++;
                            r2--;
                        } else {
                            h1++;
                            h2++;
                        }
                    } else if (h2 == r2) {
                        if (nums2[h2] > nums1[h1] && nums2[h2] < nums1[r1]) {
                            h1++;
                            r1--;
                        } else if (nums2[h2] <= nums1[h1]) {
                            h2++;
                            r1--;
                        } else {
                            h2++;
                            h1++;
                        }
                    }
                    continue;
                }
                // 获取移除间隔
                int diff = r1 - h1 - 1;
                if (diff > r2 - h2 - 1) {
                    diff = r2 - h2 - 1;
                }
                // 获取中位数
                int hIdx1 = 0, rIdx1 = 0;
                checkArrayMedian(nums1, h1, r1, diff, out hIdx1, out rIdx1);
                int hIdx2 = 0, rIdx2 = 0;
                checkArrayMedian(nums2, h2, r2, diff, out hIdx2, out rIdx2);
                Console.WriteLine("---hIdx1: {0}, rIdx1: {1}; hIdx2: {2}, rIdx2: {3};---", hIdx1, rIdx1, hIdx2, rIdx2);
                // 去掉头部
                if (nums1[hIdx1] < nums2[hIdx2]) {
                    h1 = hIdx1 + 1;
                } else {
                    h2 = hIdx2 + 1;
                }
                // 去掉尾部
                if (nums1[rIdx1] > nums2[rIdx2]) {
                    r1 = rIdx1 - 1;
                } else {
                    r2 = rIdx2 - 1;
                }
            }
            // 返回结果
            if (h1 == r1 && h2 == r2) {
                return (double) (nums1[h1] + nums2[h2]) / 2;
            } else if (h1 == r1) {
                return (double) nums1[h1];
            } else if (h2 == r2) {
                return (double) nums2[h2];
            }
            // 获取中位数
            int h = h1, r = r1;
            int[] nums = nums1;
            if (h1 > r1) {
                h = h2;
                r = r2;
                nums = nums2;
            }
            int hIdx = 0, rIdx = 0;
            checkArrayMedian(nums, h, r, r - h - 1, out hIdx, out rIdx);
            StringBuilder str = new StringBuilder();
            Console.WriteLine("nums: [{0}], h: {1}, r: {2}, hIdx: {3}, rIdx: {4}", str.AppendJoin(',', nums), h, r, hIdx, rIdx);
            if (rIdx - hIdx == 2) {
                return nums[hIdx+1];
            }
            return (double) (nums[hIdx] + nums[rIdx]) / 2;
        }
    }
}