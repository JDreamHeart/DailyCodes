using System;
using System.Collections;
using System.Collections.Generic;

namespace LeetCode{
    public class Solution {
        public bool IsMatch(string s, string p) {
            return matchSubStr(s, p, 0, 0);
        }
        private bool matchSubStr(string s, string p, int i, int j) {
            while (i < s.Length && j < p.Length) {
                // 下一个是'*'，则先跳过下一个字符检测
                if (j+1 < p.Length && p[j+1] == '*') {
                    if (matchSubStr(s, p, i, j+2)) {
                        return true;
                    }
                }
                if (isMatchChar(s[i], p[j])) {
                    j++;
                    // 判断是否字符串都遍历完
                    if (++i == s.Length) {
                        break;
                    }
                    // 判断匹配成功的字符串后一个是否为'*'，是的话，递归匹配0或当前成功后的字符串
                    if (j < p.Length && p[j] == '*') {
                        if (matchSubStr(s, p, i, j+1)) {
                            return true;
                        }
                        j--;
                    }
                } else {
                    // 未匹配成功，且下一个是'*'，则跳过下两个字符【一位在一开始已经查找过跳过第一个字符的情况了】
                    if (++j < p.Length && p[j] == '*') {
                        j+=2;
                    }
                }
            }
            return isEndMatch(s, p, i, j);
        }
        private bool isMatchChar(char sc, char pc) {
            if (pc == '.') {
                return true;
            }
            return sc == pc;
        }
        private bool isEndMatch(string s, string p, int i, int j) {
            if (i == s.Length && j <= p.Length) {
                if (j == p.Length - 1) {
                    j--;
                }
                // 判断是否还有字符串未匹配完，且能匹配成功
                for (int k = 1; k < p.Length - j; k+=2) {
                    if (p[k+j] != '*' || k+j == p.Length - 2) {
                        return false;
                    }
                }
                return true;
            }
            return false;
        }

        // 新匹配方式
        public bool isMatchS(string s, string p) {
            // 分离模式
            List<int> newP;
            Hashtable ht;
            newP = splitPattern(p, out ht);
            // 开始匹配模式
            int startIdx = 0;
            int endIdx = 0;
            foreach (char c in s) {
                for (int i = startIdx; i < newP.Count; i ++) {
                    
                }
            }
            return matchSubStr(s, p, 0, 0);
        }

        private List<int> splitPattern(string p, out Hashtable ht) {
            List<int> newP = new List<int>{};
            ht = new Hashtable();
            for (int i = 0; i < p.Length; i ++) {
                if (p[i] != '*') {
                    newP.Add(p[i]);
                } else if (i - 1 >= 0) {
                    ht.Add(newP.Count - 1, true);
                }
            }
            return newP;
        }
    }
}