"""
Problem: Sell Diminishing-Valued Colored Balls

Description:
You have an inventory of different colored balls, and there is a customer that wants orders orders. The customer can buy any colored ball of your choice for a price equal to the number of balls of that color you currently have. After the customer buys a ball, the number of balls of that color decreases by 1. Return the maximum total value that you can attain after selling orders balls. Return it modulo 10^9 + 7.

Constraints:
1 <= inventory.length <= 10^5, 1 <= inventory[i] <= 10^9, 1 <= orders <= min(sum(inventory), 10^9).

Example:
Input: inventory = [2,5], orders = 4 -> Output: 14
"""

class Solution:
    def maxProfit(self, inventory: List[int], orders: int) -> int:
        pass
