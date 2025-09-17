from langsmith.wrappers import wrap_openai

from prompt import agent_coder_prompt
from utils import read_problems, write_jsonl
from openai import OpenAI
from openai import AuthenticationError, RateLimitError, APIError, InternalServerError
import os
import re
from dotenv import load_dotenv
from tqdm import tqdm
from execution import check_correctness

load_dotenv()


def remove_think_part(text):
    # 提取回复中的Python 代码块

    # 首先判断是否包含```python
    if "```python" not in text:
        return text

    pattern = r"```python\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        cleaned_text = match.group(1).strip()
        return cleaned_text.strip()
    else:
        # 有```python但正则没匹配到，返回空字符串
        return "def check(candidate):\n    assert True == False"


class NoneTestCasesException(Exception):
    def __init__(self, message="No test cases found"):
        self.message = message
        super().__init__(self.message)


def generate_completion(model: str, prompt: list, enable_thinking: bool = True):
    client = wrap_openai(OpenAI(base_url=os.getenv("OPENAI_BASE_URL")))
    try:
        response = client.chat.completions.create(
            model=model,
            messages=prompt,
            extra_body={"chat_template_kwargs": {"enable_thinking": enable_thinking}},
        )
        completion = response.choices[0].message.content
        return completion
    except (
        AuthenticationError,
        RateLimitError,
        APIError,
        InternalServerError,
    ) as e:
        print(f"OpenAI API Error: {e}")
        raise NoneTestCasesException
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise NoneTestCasesException


def process_problems(problems: dict, model: str, enable_thinking: bool = True):
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
                model, [{"role": "user", "content": prompt}], enable_thinking
            )
            if completion:
                test_cases = remove_think_part(completion)
                result = check_correctness(problem, test_cases)
                if result["passed"]:
                    passed_generate_test.append(
                        {"task_id": task_id, "test_cases": test_cases}
                    )
                else:
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
    # model = "Qwen/Qwen3-8B"
    enable_thinking = True
    model = "gpt-5-2025-08-07"
    # 限制 problems 数量为前 10 个
    # problems = dict(list(problems.items())[:2])
    process_problems(problems, model, enable_thinking)


if __name__ == "__main__":
    main()
