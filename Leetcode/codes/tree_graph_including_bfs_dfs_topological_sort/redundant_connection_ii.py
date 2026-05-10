"""
Problem: Redundant Connection II

Description:
In this problem, a rooted tree is a directed graph such that, there is exactly one node (the root) for which all other nodes are descendants of this node, plus every node has exactly one parent, except for the root node which has no parents. The given input is a directed graph that started as a rooted tree with n nodes (with distinct values from 1 to n), with one additional directed edge added. Return an edge that can be removed so that the resulting graph is a rooted tree of n nodes.

Constraints:
n == edges.length, 3 <= n <= 1000, edges[i].length == 2, 1 <= ui, vi <= n.

Example:
Input: edges = [[1,2],[1,3],[2,3]] -> Output: [2,3]
"""

class Solution:
    def findRedundantDirectedConnection(self, edges: List[List[int]]) -> List[int]:
        pass
