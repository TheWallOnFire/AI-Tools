"""
Problem: Invalid Transactions

Description:
A transaction is possibly invalid if: the amount exceeds $1000, or if it occurs within (and including) 60 minutes of another transaction with the same name in a different city. Return a list of all possibly invalid transactions.

Constraints:
transactions.length <= 1000, each transaction is a string "name,time,amount,city".

Example:
Input: transactions = ["alice,20,800,mtv","alice,50,100,beijing"] -> Output: ["alice,20,800,mtv","alice,50,100,beijing"]
"""

class Solution:
    def invalidTransactions(self, transactions: List[str]) -> List[str]:
        pass
