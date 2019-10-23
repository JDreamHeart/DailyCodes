using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;

namespace LeetCode{
    public class Solution2 {
        private int[] numList = {1000, 100, 10, 1};
        private string[] strList = {"M", "C", "X", "I"};
        private string[] extStrList = {"", "D", "L", "V"};
        private Hashtable ht = new Hashtable();
        public Solution() {
            // 初始化ht
            ht.Add(4, "IV");
            ht.Add(9, "IX");
            ht.Add(40, "XL");
            ht.Add(90, "XC");
            ht.Add(400, "CD");
            ht.Add(900, "CM");
        }
        public string IntToRoman(int num) {
            StringBuilder str = new StringBuilder();
            int tmp;
            for (int i = 0; i < numList.Length; i ++) {
                tmp = (int) num/numList[i];
                num -= tmp * numList[i];
                if (this.ht.Contains(tmp * numList[i])) {
                    str.Append((string) ht[tmp*numList[i]]);
                } else {
                    if (tmp >= 5 && extStrList[i] != "") {
                        str.Append(extStrList[i]);
                        tmp -= 5;
                    }
                    toRoman(tmp, strList[i], str);
                }
            }
            return str.ToString();
        }
        private void toRoman(int n, string s, StringBuilder str) {
            for (int i = 0; i < n; i ++) {
                str.Append(s);
            }
        }
    }
}