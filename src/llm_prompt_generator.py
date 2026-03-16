# cd ~/llm-parser
# source venv/bin/activate
# python3 llm_prompt_generator.py

import json
import openai

def load_parsed_reports(json_path):
    with open(json_path, "r") as f:
        return json.load(f)

def build_prompt(parsed_data):
    prompt = "You are an expert FPGA design assistant.\n"
    prompt += "Given the following implementation reports, summarize key insights and provide possible optimization suggestions.\n\n"

    for filename, report in parsed_data.items():
        prompt += f"--- {filename} ---\n"
        prompt += json.dumps(report, indent=2)
        prompt += "\n\n"

    prompt += "Please summarize the timing, utilization, power and log status. If any problems are found (e.g. negative slack, critical warnings), suggest fixes.\n"
    return prompt

# setup OpenAI API Key
client = openai.OpenAI(
    api_key="" # use your own Key
)

def query_llm(prompt):
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a hardware synthesis and FPGA analysis expert."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3,
    max_tokens=1000
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    parsed = load_parsed_reports("/home/april-ai/parsed_all_reports.json")
    prompt = build_prompt(parsed)
    print("🔍 Sending the following prompt to GPT:\n")
    print(prompt)

    reply = query_llm(prompt)
    print("\n🤖 LLM Response:\n")
    print(reply)
