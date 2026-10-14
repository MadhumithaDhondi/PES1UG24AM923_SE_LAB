# Reflection – Lab 5: Static Code Analysis

## 1. What did you learn from static code analysis?

I learned that static code analysis tools can identify code quality, formatting, reliability, and security problems without requiring the program to be executed. Pylint helped me improve code quality and readability, Flake8 identified style and formatting issues, and Bandit helped identify potential security vulnerabilities. Using these tools made the code easier to maintain and safer.

## 2. What were the most important issues you identified?

The most important issues were the hardcoded ERP API key, disabled SSL certificate verification, unsafe command execution, and the lack of a timeout for network requests. These problems could expose sensitive information, weaken secure communication, or cause the program to behave unreliably. I also corrected attendance-register handling and improved naming and documentation.

## 3. How did you fix the identified issues?

I removed the hardcoded API key and used an environment variable instead. I restored secure HTTPS certificate verification, added a timeout to network requests, and replaced unsafe shell-based command execution with safer handling. I also corrected the attendance-register logic, improved function naming and documentation, and fixed the formatting and lint issues reported by the analysis tools.

## 4. How did you verify that your changes were successful, and what did you learn?

I reran the program and all three static analysis tools after making the changes. The program executed successfully and displayed the expected demonstration output. Pylint reported a score of 10.00/10, Bandit reported zero high-, medium-, and low-severity findings, and Flake8 reported no style errors. I learned that static analysis is useful for finding problems early, but its results should also be checked against program behavior and the intended requirements.
