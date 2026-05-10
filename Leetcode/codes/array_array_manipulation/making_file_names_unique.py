"""
Problem: Making File Names Unique

Description:
Given an array of strings names of size n. You will create n folders one by one. If a folder name is already used, you will append (k) to the end where k is the smallest positive integer such that the obtained name has not been used before. Return an array of strings of length n where names[i] is the actual name the system will assign to the i-th folder.

Constraints:
1 <= names.length <= 5 * 10^4, 1 <= names[i].length <= 20, names[i] consists of lowercase English letters, digits and/or round brackets.

Example:
Input: names = ["pes","pes","pes","pes"] -> Output: ["pes","pes(1)","pes(2)","pes(3)"]
"""

class Solution:
    def getFolderNames(self, names: List[str]) -> List[str]:
        pass
