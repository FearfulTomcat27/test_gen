# AI 测试用例生成器

[English](README.md) | 中文

一个基于 Python 的系统，利用 AI 模型（Claude/OpenAI）为 HumanEval 数据集中的编程函数自动生成全面的测试用例。

## 🚀 功能特性

- **AI 驱动的测试生成**：使用 Claude 或 OpenAI 模型生成智能测试用例
- **执行验证**：自动运行生成的测试用例以验证正确性
- **全面覆盖**：为每个函数生成 5 个测试用例，涵盖正常和边缘情况
- **优雅中断**：支持 Ctrl+C 中断并跟踪进度
- **Token 使用跟踪**：监控和报告 API token 消耗
- **结果分类**：将结果分类为通过、失败和生成失败的用例

## 📁 项目结构

```
test_gen/
├── main.py              # 主执行逻辑和协调
├── utils.py             # API 调用和文件操作的工具函数
├── prompt.py            # 测试生成的 AI 提示模板
├── execution.py         # 安全代码执行和验证系统
├── execptions.py        # 自定义异常定义
├── data.jsonl           # HumanEval 数据集（164个编程问题）
├── .env                 # 环境变量（API 密钥）
├── README.md           # 项目文档（英文）
└── README_zh.md        # 项目文档（中文）
```

## 🛠️ 安装

1. 克隆仓库：
```bash
git clone <repository-url>
cd test_gen
```

2. 安装依赖：
```bash
pip install python-dotenv tqdm anthropic openai langsmith
```

3. 在 `.env` 文件中设置环境变量：
```bash
ANTHROPIC_API_KEY=你的_anthropic_api_密钥
OPENAI_API_KEY=你的_openai_api_密钥  # 可选
OPENAI_BASE_URL=你的_openai_base_url  # 可选
```

## 🎯 使用方法

### 基本使用

在 HumanEval 数据集上运行测试生成器：

```bash
python main.py
```

### 配置

编辑 `main.py` 进行自定义：

- **模型选择**：在 Claude 和 OpenAI 模型之间选择
- **数据集大小**：限制要处理的问题数量
- **输出文件**：自定义结果文件名

```python
# 在 main.py 中
model = "claude-3-7-sonnet-20250219"  # 或 "gpt-4" 使用 OpenAI
problems = dict(list(problems.items())[:10])  # 处理前 10 个问题
```

### 中断执行

按 `Ctrl+C` 优雅地中断进程。系统将：
- 停止生成新的测试用例
- 显示当前进度统计
- **不写入**结果文件（防止部分数据）
- 显示每个类别的计数

## 📊 输出文件

当执行正常完成时，会生成三个文件：

1. **`passed_test_problem.jsonl`**：测试用例通过执行的函数
2. **`failed_test_problems.jsonl`**：测试用例执行失败的函数
3. **`generate_failed_problems.jsonl`**：测试生成失败的函数

每个条目包含：
```json
{
  "task_id": "HumanEval/0",
  "prompt": "函数描述...",
  "canonical_solution": "参考实现...",
  "test_cases": "生成的测试代码...",
  "entry_point": "函数名"
}
```

## 🧠 AI 提示策略

系统使用精心设计的提示，指导 AI：

1. **分析**函数需求和参数
2. **规划**涵盖正常和边缘场景的测试用例
3. **生成**正好 5 个多样化的测试断言
4. **确保**准确性，包含正确的预期输出
5. **验证**语法和性能约束

## 🔧 架构

### 核心组件

- **`process_problems()`**：主要协调循环
- **`process_one_task()`**：处理单个函数的处理
- **`generate_completion()`**：AI API 集成，包含错误处理
- **`check_correctness()`**：安全代码执行和验证
- **`remove_think_part()`**：从 AI 响应中提取 Python 代码

### 安全特性

- **沙盒执行**：使用 `execution.py` 进行安全代码运行
- **超时保护**：每个测试 10 秒执行限制
- **错误隔离**：失败不会导致整个进程崩溃
- **资源限制**：内存和系统调用限制

## 📈 性能

- **Token 跟踪**：监控 API 使用和成本
- **进度可视化**：使用 tqdm 实时显示进度
- **批处理**：高效处理大型数据集
- **错误恢复**：API 过载错误时自动重试

## 🚨 错误处理

系统处理各种错误场景：

- **API 失败**：速率限制、身份验证、服务器错误
- **生成失败**：无效或空的 AI 响应
- **执行错误**：语法错误、运行时异常、超时
- **中断**：用户中断的优雅处理

## 🔍 示例输出

```bash
100%|██████████| 164/164 [2:15:30<00:00, 49.57s/it]
本次总共使用 token 892456
Passed generate test: 89
Failed generate test: 67
Generate fail id: 8
```

## 🛡️ 注意事项

- 确保 API 密钥的安全性，不要将其提交到版本控制
- 系统会消耗 API token，请监控使用情况
- 代码执行在沙盒环境中进行，但仍建议在隔离环境中运行
- 大数据集处理可能需要较长时间，建议分批处理

## 🤝 贡献

1. Fork 仓库
2. 创建功能分支
3. 进行更改
4. 如适用，添加测试
5. 提交 pull request

## 📄 许可证

此项目是学术研究的一部分，遵循标准开源实践。

## 🙏 致谢

- 基于 HumanEval 数据集进行代码生成评估
- 集成了 Anthropic Claude 和 OpenAI API
- 使用 LangSmith 进行 API 监控和调试