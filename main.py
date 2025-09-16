from prompt import agent_coder_prompt
from utils import read_problems, write_jsonl
from openai import OpenAI
from openai import AuthenticationError, RateLimitError, APIError, InternalServerError
import os
import re
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()


def remove_think_part(text):
    # 提取回复中的Python 代码块
    pattern = r"```python\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        cleaned_text = match.group(1).strip()
    else:
        cleaned_text = ""
    return cleaned_text.strip()


class NoneTestCasesException(Exception):
    def __init__(self, message="No test cases found"):
        self.message = message
        super().__init__(self.message)


def generate_completion(model: str, prompt: list):
    client = OpenAI(base_url=os.getenv("OPENAI_BASE_URL"))
    try:
        response = client.chat.completions.create(model=model, messages=prompt)
        completion = response.choices[0].message.content
    except (
        AuthenticationError,
        RateLimitError,
        APIError,
        InternalServerError,
    ) as e:
        print(f"OpenAI API Error: {e}")
        completion = ""
        raise NoneTestCasesException
    except Exception as e:
        print(f"Unexpected error: {e}")
        completion = ""
        raise NoneTestCasesException
    finally:
        return completion


def check_correction(check_program: str):
    status_code = -1
    try:
        exec(check_program)
        status_code = 0
    except BaseException as e:
        print(f"Test Code:\n{check_program}")
        print(f"Test execution erro : {e}")
        status_code = 1
    finally:
        return status_code


def process_problems(problems: dict, model: str):
    # 成功通过的用例
    passed_generate_test = []
    # 成功生成但不通过的用例
    failed_generate_test = []
    # 生成失败的task_id
    generate_fail_id = []

    for task_id in tqdm(problems):
        problem = problems[task_id]
        prompt = agent_coder_prompt.format(
            function_name=problem["entry_point"], function_requirement=problem["prompt"]
        )

        try:
            completion = generate_completion(
                model, [{"role": "user", "content": prompt}]
            )
            if completion:
                test_cases = remove_think_part(completion)
                check_program = (
                    problem["prompt"]
                    + problem["canonical_solution"]
                    + "\n"
                    + test_cases
                    + "\n"
                    + f"check({problem['entry_point']})"
                )
                status_code = check_correction(check_program)
                if status_code == 0:
                    print(f"Test passed for {task_id}")
                    passed_generate_test.append(
                        {"task_id": task_id, "test_cases": test_cases}
                    )
                else:
                    print(f"Test failed for {task_id}")
                    failed_generate_test.append(
                        {"task_id": task_id, "test_cases": test_cases}
                    )
            else:
                generate_fail_id.append({"task_id": task_id, "test_cases": ""})
        except NoneTestCasesException as e:
            print(f"NoneTestCasesException for {task_id}: {e}")
            generate_fail_id.append({"task_id": task_id, "test_cases": ""})

    write_jsonl(f"pass_generate_test.jsonl", passed_generate_test)
    print(f"Passed generate test: {len(passed_generate_test)}")
    write_jsonl(f"failed_generate_test.jsonl", failed_generate_test)
    print(f"Failed generate test: {len(failed_generate_test)}")
    write_jsonl(f"generate_fail_id.jsonl", generate_fail_id)
    print(f"Generate fail id: {len(generate_fail_id)}")


def main():
    problems = read_problems()
    # model = "qwen/qwen3-8b:free"
    model = "Qwen/Qwen3-8B"
    # 限制 problems 数量为前 10 个
    problems = dict(list(problems.items())[:2])
    process_problems(problems, model)


if __name__ == "__main__":
    main()
