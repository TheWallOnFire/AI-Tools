"""
Problem: Maximum Score from Performing Multiplication Operations

Description:
You are given two integer arrays nums and multipliers of size n and m respectively, where n >= m. You begin with a score of 0. You want to perform exactly m operations. On the i-th operation (0-indexed), you will: Choose one integer x from either the start or the end of the array nums; Add multipliers[i] * x to your score; Remove x from nums.

Constraints:
n == nums.length, m == multipliers.length, 1 <= m <= 10^3, m <= n <= 10^5, -1000 <= nums[i], multipliers[i] <= 1000.

Example:
Input: nums = [1,2,3], multipliers = [3,2,1] -> Output: 14
"""

class Solution:
    def maximumScore(self, nums: List[int], multipliers: List[int]) -> int:
        pass
