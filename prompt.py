agent_coder_prompt = """
**Role**: As a tester, your task is to create five additional unique comprehensive test cases for the incomplete {function_name} function. These test cases should encompass Basic, Edge, and Large Scale scenarios to ensure the code'srobustness, reliability, and scalability.

**Input Code Snippet**:
```python
{function_requirement}
```

**1. Basic Test Cases**:
- **Objective**: To verify the fundamental functionality of the {function_name} function under normalconditions.

**2. Edge Test Cases**:
- **Objective**: To evaluate the function's behavior under extreme or unusual conditions.

**3. Large Scale Test Cases**:
- **Objective**: To assess the function's performance and scalability with large data samples.

**Instructions**:
- Implement a comprehensive set of test cases following the guidelines above.
- Ensure each test case is well-documented with comments explaining the scenario it covers.
- Pay special attention to edge cases as they often reveal hidden bugs.
- For large-scale tests, focus on the function's efficiency and performance under heavy loads.

**Requirements**
- Each test case should be on a new line
- Ensure test cases satisfy the solution's logic
- Use valid Python syntax
- Do not include any explanations or comments within the test case code

**Output Format**:
```python
def check(candidate):
    assert candidate(input) == output
    assert candidate(input) == output
    assert candidate(input) == output
    assert candidate(input) == output
    assert candidate(input) == output
```
"""
