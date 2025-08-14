# response_monitor.py

import json
import os
from datetime import datetime

LOG_FILE = "response_log.json"

def record_response(instructions, input, openai_response):
    usage = getattr(openai_response, "usage", None)

    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "input": input,
        "instructions": instructions,
        "model": getattr(openai_response, "model", "unknown"),
        "output": openai_response.choices[0].message.content if openai_response.choices else "",
        "tokens": {
            "input_tokens": usage.prompt_tokens if usage else None,
            "output_tokens": usage.completion_tokens if usage else None,
            "total_tokens": usage.total_tokens if usage else None
        }
    }

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([log_entry], f, indent=2)
    else:
        with open(LOG_FILE, "r+") as f:
            data = json.load(f)
            data.append(log_entry)
            f.seek(0)
            json.dump(data, f, indent=2)

    print(f"✅ Response recorded in {LOG_FILE}")
