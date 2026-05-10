"""
Problem: Word Ladder II

Description:
A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that: Every adjacent pair of words differs by a single letter. Every si for 1 <= i <= k is in wordList. Return all the shortest transformation sequences from beginWord to endWord, or an empty list if no such sequence exists.

Constraints:
1 <= beginWord.length <= 5, wordList.length <= 500, beginWord, endWord, and wordList[i] consist of lowercase English letters.

Example:
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"] -> Output: [["hit","hot","dot","dog","cog"],["hit","hot","lot","log","cog"]]
"""

class Solution:
    def findLadders(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        pass
