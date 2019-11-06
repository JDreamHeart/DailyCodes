// 给定一个链表，删除链表的倒数第 n 个节点，并且返回链表的头结点。

// 示例：

// 给定一个链表: 1->2->3->4->5, 和 n = 2.

// 当删除了倒数第二个节点后，链表变为 1->2->3->5.

using System;
using System.Collections;
using System.Collections.Generic;

/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     public int val;
 *     public ListNode next;
 *     public ListNode(int x) { val = x; }
 * }
 */

namespace LeetCode {
    public class Solution5 {
        public ListNode RemoveNthFromEnd(ListNode head, int n) {
        ListNode preNode;
        int idx = 0;
        ListNode node = head;
        do {
            idx++;
            if (idx == n - 1) {
                preNode = node;
            } else if (idx >= n) {
                preNode = preNode.next;
            }
            node = node.next;
        } while (node.next != null);
        if (preNode != null) {
            ListNode tgNode = preNode.next;
            preNode.next = tgNode.next;
            tgNode.next = null;
        } else if (idx == n) {
            ListNode tgNode = head;
            head = head.next;
            tgNode.next = null;
        }
        return head;
    }
    }
}