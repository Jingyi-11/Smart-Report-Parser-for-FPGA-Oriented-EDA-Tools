
# Smart Report Parser for FPGA-Oriented EDA Tools

An LLM-assisted toolchain for parsing FPGA implementation reports and log files from EDA tools such as **Xilinx Vivado**, converting them into structured data, and generating **readable diagnostics** and **optimization suggestions**.

## Overview

FPGA development tools generate rich but often complex reports after synthesis and implementation, including utilization summaries, timing analysis, power estimation, and error logs. Manually reviewing these files can be time-consuming and error-prone.

This project builds a **Python-based report parser** that extracts key information from Vivado report files and log files, organizes them into structured formats such as JSON/dictionaries, and then uses a large language model (LLM) to generate:

- concise report summaries
- design diagnostics
- debugging hints
- optimization suggestions

The goal is to make FPGA post-implementation analysis more efficient, interpretable, and scalable.

## Features

- Parse **Vivado** report and log files
- Extract key design metrics from:
  - **Utilization reports**
  - **Timing reports**
  - **Power reports**
  - **Run logs**
- Convert parsed results into structured **JSON-like dictionaries**
- Generate LLM prompts with different context levels
- Use GPT-based models to produce:
  - natural-language summaries
  - debugging explanations
  - optimization recommendations
- Support interactive analysis through a simple web interface

## Project Structure

```text
smart-report-parser/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── src/
│   ├── parser/
│   │   ├── vivado_parser.py
│   │   ├── utilization_parser.py
│   │   ├── timing_parser.py
│   │   ├── power_parser.py
│   │   └── log_parser.py
│   ├── llm/
│   │   ├── prompt_generator.py
│   │   ├── llm_client.py
│   │   └── response_parser.py
│   ├── web/
│   │   └── app.py
│   ├── utils/
│   │   ├── file_loader.py
│   │   └── json_writer.py
│   └── main.py
├── examples/
│   ├── input_reports/
│   └── output_json/
├── docs/
│   ├── project_paper.pdf
│   ├── poster.pdf
│   ├── architecture.png
│   └── screenshots/
├── tests/
└── results/
```
