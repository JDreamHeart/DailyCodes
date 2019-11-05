// 给定一个仅包含数字 2-9 的字符串，返回所有它能表示的字母组合。

// 给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。

using System;
using System.Collections;
using System.Collections.Generic;

namespace LeetCode {
    public class Solution4 {
        private Hashtable dgHt = new Hashtable();
        public Solution4() {
            dgHt.Add('2', "abc");
            dgHt.Add('3', "def");
            dgHt.Add('4', "ghi");
            dgHt.Add('5', "jkl");
            dgHt.Add('6', "mno");
            dgHt.Add('7', "pqrs");
            dgHt.Add('8', "tuv");
            dgHt.Add('9', "wxyz");
        }
        public IList<string> LetterCombinations(string digits) {
            IList<string> ret = new List<string>();
            if (digits.Length > 0) {
                string[] strs = new string[digits.Length];
                for (int i = 0; i < digits.Length; i++) {
                    strs[i] = (string) dgHt[digits[i]];
                }
                combineByRecursion(strs, 0, ret, "");
            }
            return ret;
        }
        private void combineByRecursion(string[] strs, int idx, IList<string> ret, string tmp) {
            if (idx >= strs.Length) {
                ret.Add(tmp);
                return;
            }
            foreach (char s in strs[idx]) {
                combineByRecursion(strs, idx+1, ret, tmp+ s.ToString());
            }
        }
    }
}