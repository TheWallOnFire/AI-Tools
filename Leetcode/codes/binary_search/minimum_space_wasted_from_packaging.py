"""
Problem: Minimum Space Wasted From Packaging

Description:
You are given an integer array packages, where packages[i] is the weight of the i-th package. You are also given a 2D integer array boxes, where boxes[j] is an array of box sizes available from the j-th supplier. You want to choose exactly one supplier from all developers such that the total waste is minimized. Return the minimum total waste modulo 10^9 + 7, or -1 if it is impossible.

Constraints:
n == packages.length, m == boxes.length, 1 <= n <= 10^5, 1 <= m <= 10^5, 1 <= boxes[j].length <= 10^5, 1 <= packages[i], boxes[j][k] <= 10^5.

Example:
Input: packages = [2,3,5], boxes = [[4,8],[2,8]] -> Output: 6
"""

class Solution:
    def minWastedSpace(self, packages: List[int], boxes: List[List[int]]) -> int:
        pass
