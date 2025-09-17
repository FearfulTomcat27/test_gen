agent_coder_prompt = """
**Role**: As a professional software tester, create exactly 5 comprehensive test cases for the {function_name} function. Your test cases must cover diverse scenarios to thoroughly validate the function's correctness, edge case handling, and performance.

**Function to Test**:
```python
{function_requirement}
```

**Test Case Categories** (aim for this distribution):
- **2-3 Basic Cases**: Normal inputs with typical expected behavior
- **1-2 Edge Cases**: Boundary conditions, empty inputs, extreme values, or unusual scenarios

**Critical Requirements**:
1. **Accuracy**: Each test case MUST produce the correct expected output for the given input
2. **Diversity**: Test cases should cover different input types, ranges, and scenarios
3. **Validity**: Use only valid Python syntax with no comments or explanations in code
4. **Performance**: Each test case should execute within 3 seconds
5. **Independence**: Each assert statement should test a unique scenario

**Quality Guidelines**:
- Consider boundary values (empty, zero, negative)
- Test different data types and structures where applicable
- Include both simple and complex inputs
- Ensure outputs are precisely calculated and correct
- Avoid redundant or overly similar test cases

**Output Format** (exactly 5 assert statements):
```python
def check(candidate):
    assert candidate(input1) == expected_output1
    assert candidate(input2) == expected_output2
    assert candidate(input3) == expected_output3
    assert candidate(input4) == expected_output4
    assert candidate(input5) == expected_output5
```

**Important**: Replace `input1, input2, etc.` and `expected_output1, expected_output2, etc.` with actual values. Do not include any text explanations outside the code block.
"""
