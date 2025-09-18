from dotenv import load_dotenv
from tqdm import tqdm

from execptions import NoneTestCasesException
from execution import check_correctness
from prompt import prompt_template
from utils import read_problems, write_jsonl, generate_completion, remove_think_part

load_dotenv()


def process_one_task(task_id: str, problem: dict, model: str):
    prompt = prompt_template.format(
        function_name=problem["entry_point"],
        function_requirement=problem["prompt"],
    )

    try:
        completion, used_token = generate_completion(
            model, [{"role": "user", "content": prompt}]
        )
        if completion:
            test_cases = remove_think_part(completion)
            result = check_correctness(problem, test_cases)
            problem["test_cases"] = test_cases
            if result["passed"]:
                return "passed", problem, used_token
            else:
                return "failed", problem, used_token
        else:
            print(f"generation failed for {task_id}")
            return "generate_fail", problem, used_token
    except NoneTestCasesException as e:
        print(f"NoneTestCasesException for {task_id}: {e}")
        return "generate_fail", problem, 0


def process_problems(problems: dict, model: str):
    # 成功通过的用例
    passed_test_problem = []
    # 成功生成但不通过的用例
    failed_test_problems = []
    # 生成失败的task_id
    generate_failed_problems = []

    interrupted = False

    total_token = 0

    try:
        for task_id in tqdm(problems):
            problem = problems[task_id]
            status, data, used_token = process_one_task(task_id, problem, model)
            total_token += used_token

            if status == "passed":
                passed_test_problem.append(data)
            elif status == "failed":
                failed_test_problems.append(data)
            elif status == "generate_fail":
                generate_failed_problems.append(data)

    except KeyboardInterrupt:
        # 当中断执行的时候还是记录通过个数
        print("\n用户中断程序执行")
        interrupted = True
    finally:
        if not interrupted:
            # 如果中断执行，则不写入文件
            write_jsonl(f"passed_test_problem.jsonl", passed_test_problem)
            write_jsonl(f"failed_test_problems.jsonl", failed_test_problems)
            write_jsonl(f"generate_failed_problems.jsonl", generate_failed_problems)

        print(f"本次总共使用 token {total_token}")
        print(f"Passed generate test: {len(passed_test_problem)}")
        print(f"Failed generate test: {len(failed_test_problems)}")
        print(f"Generate fail id: {len(generate_failed_problems)}")


def main():
    problems = read_problems()
    model = "claude-3-7-sonnet-20250219"
    # 限制 problems 数量为前 10 个
    # problems = dict(list(problems.items())[:10])
    process_problems(problems, model)


if __name__ == "__main__":
    main()
