# Multitasking Agent

This project provides an interactive CLI tool for software engineering tasks, capable of executing multiple tasks in parallel.

## Setup
Before you start, ensure Python 3.10 or above is installed. Store your Gemini API key in the environment:

```
export GEMINI_API_KEY="MY_API_KEY"
```

Install the package everywhere, run this without a virtual environment activated:

```
pip install -e .
```

To uninstall the package everywhere:

```
pip uninstall multitasking-agent
```

## Usage
Navigate to your project directory. To run some instructions:

```
agent "Write python code that generates five random numbers between 1 to 6."
```