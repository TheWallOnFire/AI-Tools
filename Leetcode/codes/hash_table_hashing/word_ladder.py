"""
Problem: Word Ladder

Description:
A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that: Every adjacent pair of words differs by a single letter. Every si for 1 <= i <= k is in wordList. Return the number of words in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.

Constraints:
1 <= beginWord.length <= 10, wordList.length <= 5000, beginWord, endWord, and wordList[i] consist of lowercase English letters.

Example:
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"] -> Output: 5
"""

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        pass
