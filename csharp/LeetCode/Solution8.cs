// 给你一个字符串 s 和一个字符规律 p，请你来实现一个支持 '.' 和 '*' 的正则表达式匹配。

// '.' 匹配任意单个字符
// '*' 匹配零个或多个前面的那一个元素
// 所谓匹配，是要涵盖 整个 字符串 s的，而不是部分字符串。

// 说明:

// s 可能为空，且只包含从 a-z 的小写字母。
// p 可能为空，且只包含从 a-z 的小写字母，以及字符 . 和 *。
// 示例 1:

// 输入:
// s = "aa"
// p = "a"
// 输出: false
// 解释: "a" 无法匹配 "aa" 整个字符串。
// 示例 2:

// 输入:
// s = "aa"
// p = "a*"
// 输出: true
// 解释: 因为 '*' 代表可以匹配零个或多个前面的那一个元素, 在这里前面的元素就是 'a'。因此，字符串 "aa" 可被视为 'a' 重复了一次。
// 示例 3:

// 输入:
// s = "ab"
// p = ".*"
// 输出: true
// 解释: ".*" 表示可匹配零个或多个（'*'）任意字符（'.'）。
// 示例 4:

// 输入:
// s = "aab"
// p = "c*a*b"
// 输出: true
// 解释: 因为 '*' 表示零个或多个，这里 'c' 为 0 个, 'a' 被重复一次。因此可以匹配字符串 "aab"。
// 示例 5:

// 输入:
// s = "mississippi"
// p = "mis*is*p*."
// 输出: false

using System;
using System.Collections;
using System.Collections.Generic;


namespace LeetCode {
    public class Solution8 {
        public bool IsMatch(string s, string p) {
            return false;
        }
        
        Dictionary<char, int> buildBc(string p) {
            Dictionary<char, int> ret = new Dictionary<char, int>();
            for (int i = 0; i < p.Length; i++) {
                ret[p[i]] = i;
            }
            return ret;
        }

        int movebyBc(string subStr, string p, Dictionary<char, int> bc) {
            for (int i = subStr.Length; i >= 0; i++) {
                if (subStr[i] != p[i]) {
                    // 坏字符在主串中的下标 - 模式串中对应的坏字符下标
                    int idx = -1; // 模式串中对应的坏字符下标
                    char c = subStr[i];
                    if (bc.ContainsKey(c)) {
                        idx = bc[c];
                    }
                    return i - idx;
                }
            }
            return -1; // 表示没有坏字符，在开始位置就匹配了
        }

        int[] buildGs(string p, out bool[] prefix) {
            prefix = new bool[p.Length];
            int[] suffix = new int[p.Length];
            for (int i = 0; i < p.Length; i++) {
                suffix[i] = -1;
            }
            int j = 0, k = 0;
            for (int i = 0; i < p.Length - 1; i++) {
                j = i;
                k = 0;
                while (j >= 0 && p[j] == p[p.Length - 1 - k]) {
                    j--;
                    k++;
                    suffix[k] = j + 1;
                }
                if (j == -1) {
                    prefix[k] = true;
                }
            }
            return suffix;
        }

        int movebyGs(int bcIdx, int pLen, int[]suffix, bool[] prefix) {
            int dsLen = pLen - bcIdx - 1;
            if (suffix[dsLen] != -1) {
                return bcIdx - suffix[dsLen] - 1;
            }
            for (int i = bcIdx + 2; i < pLen; i++) {
                if (prefix[pLen - i]) {
                    return i;
                }
            }
            return pLen;
        }
    }
}