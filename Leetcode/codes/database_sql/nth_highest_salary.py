"""
Problem: Nth Highest Salary

Description:
Write a SQL query to get the n-th highest salary from the Employee table.

Constraints:
Employee table has columns Id and Salary.

Example:
Input: n = 2, Employee = [[1, 100], [2, 200], [3, 300]] -> Output: 200
"""

CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
  RETURN (
      # Write your MySQL query statement below.
  );
END
