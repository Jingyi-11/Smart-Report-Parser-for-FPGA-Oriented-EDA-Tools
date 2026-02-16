import os
import re
import json

def detect_report_type(content):
    if "Total On-Chip Power" in content:
        return "power"
    elif "Slice LUTs" in content or "LUT as Logic" in content:
        return "utilization"
    elif "Slack" in content and "Data Path Delay" in content:
        return "timing"
    elif "Vivado" in content and "INFO:" in content:
        return "log"
    else:
        return "unknown"

# Power Report Parser
def parse_power_report(content):
    # with open(file_path, 'r') as f:
    #     content = f.read()

    power_data = {"type": "power"}

    # total power
    total_match = re.search(r'Total On-Chip Power.*?([\d\.]+)', content)
    dynamic_match = re.search(r'Dynamic.*?([\d\.]+)', content)
    static_match = re.search(r'Static Power.*?([\d\.]+)', content)

    power_data['Total'] = float(total_match.group(1)) if total_match else None
    power_data['Dynamic'] = float(dynamic_match.group(1)) if dynamic_match else None
    power_data['Static'] = float(static_match.group(1)) if static_match else None

    return power_data


# Resource / Utilization Report Parser
def parse_utilization_report(content):
    result = {"type": "utilization"}  # result is dictionary

    def extract_resource(content, name):
        # resource name、used、available、utiliazation (%)
        pattern = rf'{name}\s*\|\s*(\d+)\s*\|\s*\d+\s*\|\s*\d+\s*\|\s*(\d+)\s*\|\s*([<>]?\d+\.\d+)\s*\|'
        match = re.search(pattern, content)
        if match:
            return {
                "used": int(match.group(1)),
                "available": int(match.group(2)),
                "utilization_percentage": float(match.group(3).replace("<", "0"))  # address "<0.01"
            }
        else:
            return {"used": 0, "available": 0, "utilization_percentage": 0.0}

    resources = {
        "luts": extract_resource(content, "Slice LUTs"),             # lookup table
        "registers": extract_resource(content, "Slice Registers"),   # register
        "bram": extract_resource(content, "Block RAM Tile"),         # block RAM
        "dsp": extract_resource(content, "DSPs"),                    # DSP module
        "io": extract_resource(content, "Bonded IOB")                # I/O pin
    }

    result["resources"] = resources
    return result


# Timing Report Parser
def parse_timing_report(content):
    result = {"type": "timing"}

    slack_match = re.search(r'Slack(?:\s*\(VIOLATED\))?\s*:\s*(inf|[-\d.]+)', content, re.IGNORECASE)

    if slack_match:
        slack_str = slack_match.group(1)
        if slack_str.lower() == "inf":
            result["slack"] = float("inf")
        else:
            result["slack"] = float(slack_str)
    else:
        result["slack"] = None

    return result

# log parser
def parse_log_file(content):
    result = {"type": "log"}

    # extract key words：Error / Warning / Info / Completed
    result["errors"] = re.findall(r'^.*?ERROR.*$', content, re.MULTILINE)
    result["warnings"] = re.findall(r'^.*?WARNING.*$', content, re.MULTILINE)
    # result["info"] = re.findall(r'^.*?INFO.*$', content, re.MULTILINE)
    
    stage_status = {
        "synthesis_completed": False,
        "implementation_completed": False,
        "bitstream_generated": False
    }

    # stages
    if "synth_design completed successfully" in content or "Finished Synth" in content:
        stage_status["synthesis_completed"] = True

    if "place_design completed successfully" in content and "route_design completed successfully" in content:
        stage_status["implementation_completed"] = True

    if "write_bitstream completed successfully" in content:
        stage_status["bitstream_generated"] = True

    result["stage_status"] = {stage: True for stage, done in stage_status.items() if done}

    return result


# batch parser
def batch_parse_rpt(directory):
    results = {}
    for file in os.listdir(directory):
        if file.endswith(".rpt") or file.endswith(".log"):
            path = os.path.join(directory, file)
            with open(path, 'r', errors="ignore") as f:
                content = f.read()
                if file.endswith(".log"):
                    results[file] = parse_log_file(content)
                    continue

                report_type = detect_report_type(content)
                if report_type == "power":
                    results[file] = parse_power_report(content)
                elif report_type == "utilization":
                    results[file] = parse_utilization_report(content)
                elif report_type == "timing":
                    results[file] = parse_timing_report(content)
                else:
                    continue
    return results


if __name__ == "__main__":
    folder = "/home/april-ai/Desktop/test_1/test_1.runs/impl_1/"
    parsed = batch_parse_rpt(folder)

    from pprint import pprint
    for filename, data in parsed.items():
        print(f"{filename}:")
        pprint(data, indent=2, width=80)
        print()  # Add newlines to separate different files

    print("current dictionary is：", os.getcwd())
    with open("parsed_all_reports.json", "w") as f:
        json.dump(parsed, f, indent=4)
