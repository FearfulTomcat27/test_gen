import gzip
import json
import os
import re
from typing import Dict, Iterable

from anthropic import (
    Anthropic,
    AuthenticationError,
    RateLimitError,
    InternalServerError,
    APIError,
)
from anthropic.types import OverloadedError
from langsmith.wrappers import wrap_anthropic, wrap_openai
from openai import OpenAI

from execptions import NoneTestCasesException

ROOT = os.path.dirname(os.path.abspath(__file__))
HUMAN_EVAL = os.path.join(ROOT, "data.jsonl")


def read_problems(evalset_file: str = HUMAN_EVAL) -> Dict[str, Dict]:
    return {task["task_id"]: task for task in stream_jsonl(evalset_file)}


def stream_jsonl(filename: str) -> Iterable[Dict]:
    """
    Parses each jsonl line and yields it as a dictionary
    """
    if filename.endswith(".gz"):
        with open(filename, "rb") as gzfp:
            with gzip.open(gzfp, "rt") as fp:
                for line in fp:
                    if any(not x.isspace() for x in line):
                        yield json.loads(line)
    else:
        with open(filename, "r") as fp:
            for line in fp:
                if any(not x.isspace() for x in line):
                    yield json.loads(line)


def write_jsonl(filename: str, data: Iterable[Dict], append: bool = False):
    """
    Writes an iterable of dictionaries to jsonl
    """
    if append:
        mode = "ab"
    else:
        mode = "wb"
    filename = os.path.expanduser(filename)
    if filename.endswith(".gz"):
        with open(filename, mode) as fp:
            with gzip.GzipFile(fileobj=fp, mode="wb") as gzfp:
                for x in data:
                    gzfp.write((json.dumps(x) + "\n").encode("utf-8"))
    else:
        with open(filename, mode) as fp:
            for x in data:
                fp.write((json.dumps(x) + "\n").encode("utf-8"))


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


# Anthropic completion generate
def generate_completion(model: str, prompt: list):
    client = wrap_anthropic(Anthropic())
    try:
        response = client.messages.create(
            model=model,
            max_tokens=16000,
            messages=prompt,
            top_p=0.95,
            thinking={"type": "enabled", "budget_tokens": 10000},
        )
        response_obj = json.loads(response.model_dump_json())
        used_token = (
            response_obj["usage"]["input_tokens"]
            + response_obj["usage"]["output_tokens"]
        )
        for block in response.content:
            if block.type == "text":
                return block.text, used_token
    except OverloadedError as e:
        return generate_completion(model, prompt)
    except (AuthenticationError, RateLimitError, APIError, InternalServerError) as e:
        print(f"Anthropic API error: {e}")
        raise NoneTestCasesException
    except Exception as e:
        print(f"Unexpected error:{e}")
        raise NoneTestCasesException


# OpenAI completion generate
def generate_completion_openai(model: str, prompt: list, enable_thinking: bool = True):
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
