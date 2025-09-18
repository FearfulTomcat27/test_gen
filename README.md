# AI Test Case Generator

English | [中文](README_zh.md)

A Python-based system that leverages AI models (Claude/OpenAI) to automatically generate comprehensive test cases for programming functions from the HumanEval dataset.

## 🚀 Features

- **AI-Powered Test Generation**: Uses Claude or OpenAI models to generate intelligent test cases
- **Execution Validation**: Automatically runs generated test cases to verify correctness
- **Comprehensive Coverage**: Generates 5 test cases per function covering normal and edge cases
- **Graceful Interruption**: Supports Ctrl+C interruption with progress tracking
- **Token Usage Tracking**: Monitors and reports API token consumption
- **Result Classification**: Categorizes results into passed, failed, and generation-failed cases

## 📁 Project Structure

```
test_gen/
├── main.py              # Main execution logic and orchestration
├── utils.py             # Utility functions for API calls and file operations
├── prompt.py            # AI prompt templates for test generation
├── execution.py         # Safe code execution and validation system
├── execptions.py        # Custom exception definitions
├── data.jsonl           # HumanEval dataset (164 programming problems)
├── .env                 # Environment variables (API keys)
├── README.md           # Project documentation (English)
└── README_zh.md        # Project documentation (Chinese)
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd test_gen
```

2. Install dependencies:
```bash
pip install python-dotenv tqdm anthropic openai langsmith
```

3. Set up environment variables in `.env`:
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key  # Optional
OPENAI_BASE_URL=your_openai_base_url  # Optional
```

## 🎯 Usage

### Basic Usage

Run the test generator on the HumanEval dataset:

```bash
python main.py
```

### Configuration

Edit `main.py` to customize:

- **Model Selection**: Choose between Claude and OpenAI models
- **Dataset Size**: Limit the number of problems to process
- **Output Files**: Customize result file names

```python
# In main.py
model = "claude-3-7-sonnet-20250219"  # or "gpt-4" for OpenAI
problems = dict(list(problems.items())[:10])  # Process first 10 problems
```

### Interrupting Execution

Press `Ctrl+C` to gracefully interrupt the process. The system will:
- Stop generating new test cases
- Display current progress statistics
- **Not write** result files (to prevent partial data)
- Show counts for each category

## 📊 Output Files

When execution completes normally, three files are generated:

1. **`passed_test_problem.jsonl`**: Functions with test cases that pass execution
2. **`failed_test_problems.jsonl`**: Functions with test cases that fail execution
3. **`generate_failed_problems.jsonl`**: Functions where test generation failed

Each entry contains:
```json
{
  "task_id": "HumanEval/0",
  "prompt": "function description...",
  "canonical_solution": "reference implementation...",
  "test_cases": "generated test code...",
  "entry_point": "function_name"
}
```

## 🧠 AI Prompt Strategy

The system uses sophisticated prompts that instruct the AI to:

1. **Analyze** the function requirements and parameters
2. **Plan** test cases covering normal and edge scenarios
3. **Generate** exactly 5 diverse test assertions
4. **Ensure** accuracy with correct expected outputs
5. **Validate** syntax and performance constraints

## 🔧 Architecture

### Core Components

- **`process_problems()`**: Main orchestration loop
- **`process_one_task()`**: Handles individual function processing
- **`generate_completion()`**: AI API integration with error handling
- **`check_correctness()`**: Safe code execution and validation
- **`remove_think_part()`**: Extracts Python code from AI responses

### Safety Features

- **Sandboxed Execution**: Uses `execution.py` for safe code running
- **Timeout Protection**: 10-second execution limit per test
- **Error Isolation**: Failures don't crash the entire process
- **Resource Limits**: Memory and system call restrictions

## 📈 Performance

- **Token Tracking**: Monitors API usage and costs
- **Progress Visualization**: Real-time progress with tqdm
- **Batch Processing**: Efficient handling of large datasets
- **Error Recovery**: Automatic retry on API overload errors

## 🚨 Error Handling

The system handles various error scenarios:

- **API Failures**: Rate limits, authentication, server errors
- **Generation Failures**: Invalid or empty AI responses
- **Execution Errors**: Syntax errors, runtime exceptions, timeouts
- **Interruption**: Graceful handling of user interruption

## 🔍 Example Output

```bash
100%|██████████| 164/164 [2:15:30<00:00, 49.57s/it]
本次总共使用 token 892456
Passed generate test: 89
Failed generate test: 67
Generate fail id: 8
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of academic research and follows standard open-source practices.

## 🙏 Acknowledgments

- Built on the HumanEval dataset for code generation evaluation
- Integrates with Anthropic Claude and OpenAI APIs
- Uses LangSmith for API monitoring and debugging