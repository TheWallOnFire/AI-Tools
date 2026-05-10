"""
Problem: Closest Room

Description:
There is a hotel with n rooms. The rooms are represented by a 2D integer array rooms where rooms[i] = [roomIdi, sizei] denotes that there is a room with ID roomIdi and size sizei. You are also given k queries in a 2D integer array queries where queries[j] = [preferredj, minSizej]. Return an array answer of length k where answer[j] is an index i such that rooms[i] has a size of at least minSizej and |roomIdi - preferredj| is minimized.

Constraints:
n == rooms.length, k == queries.length, 1 <= n, k <= 10^5, 1 <= roomIdi, preferredj <= 10^7, 1 <= sizei, minSizej <= 10^7.

Example:
Input: rooms = [[2,2],[1,2],[3,2]], queries = [[3,1],[3,3],[5,2]] -> Output: [3,-1,3]
"""

class Solution:
    def closestRoom(self, rooms: List[List[int]], queries: List[List[int]]) -> List[int]:
        pass
