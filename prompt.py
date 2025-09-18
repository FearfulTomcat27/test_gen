agent_coder_prompt = """
**Role**: As a professional software tester, create exactly 5 comprehensive test cases for the {function_name} function. Your test cases must cover diverse scenarios to thoroughly validate the function's correctness, edge case handling, and performance.

**Function to Test**:
```python
{function_requirement}
```

**Test Case Categories** (aim for this distribution):
- **2-3 Basic Cases**: Normal inputs with typical expected behavior
- **2-3 Edge Cases**: Boundary conditions, empty inputs, extreme values, or unusual scenarios

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

prompt_template = """
You are a professional software tester tasked with creating comprehensive test cases for a Python
function. You will create exactly 5 test cases that thoroughly validate the function's correctness,
edge case handling, and performance.

Here is the function to test:

<function_name>
{function_name}
</function_name>

<function_requirement>
{function_requirement}
</function_requirement>

Before writing your test cases, use <test_planning> tags to:
1. Analyze what the function does and identify its parameters and return type
2. List potential edge cases and boundary conditions
3. Plan 2-3 basic test cases with normal inputs
4. Plan 2-3 edge cases (empty inputs, boundary values)
5. Calculate the exact expected outputs for each planned input

Your test cases must meet these critical requirements:
- **Accuracy**: Each assertion must have the correct expected output for the given input
- **Diversity**: Cover different input scenarios, data types, and ranges
- **Validity**: Use only valid Python syntax with actual values (no placeholders)
- **Performance**: Each test should complete within 3 seconds
- **Independence**: Each assert tests a unique scenario

Consider testing:
- Normal/typical inputs with expected behavior
- Boundary values (empty collections, zero, negative numbers, single elements)
- Maximum/minimum valid inputs
- Different data types or structures where applicable
- Complex or nested inputs if relevant

Your output must be exactly 5 assert statements in this format:

```python
def check(candidate):
    assert candidate(actual_input_1) == actual_expected_output_1
    assert candidate(actual_input_2) == actual_expected_output_2
    assert candidate(actual_input_3) == actual_expected_output_3
    assert candidate(actual_input_4) == actual_expected_output_4
    assert candidate(actual_input_5) == actual_expected_output_5
```

Replace all placeholders with actual Python values. Do not include comments, explanations, or any
text outside the code block in your final output.

Begin by analyzing the function in your test planning phase, then provide the test cases.
"""
