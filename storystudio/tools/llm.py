import json
import os
import re

import openai

from storystudio.settings import app_settings

openai.api_key = app_settings.OPENAI_API_KEY


def generate(prompt, model="gpt-4", max_tokens=7000):
    messages = [{"role": "user", "content": prompt}]
    kwargs = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.3,
        "n": 1,
        "stop": None,
    }
    completion = openai.ChatCompletion.create(**kwargs)

    return completion.choices[0].message["content"]


def parse_output(gpt_response, output_keys):
    """Parse the response from llm"""
    # Use regular expressions to find all JSON strings
    json_strings = re.findall("```python\n({.*?})\n```", gpt_response, re.DOTALL)

    # Initialize an empty dictionary to store the parsed JSON data
    parsed_data = {}

    for json_string in json_strings:
        # Parse each JSON string into a Python dictionary
        data = json.loads(json_string)

        # Add the parsed data to the overall dictionary
        parsed_data.update(data)
    output = {}
    for key in output_keys:
        output[key] = parsed_data[key]
    return output
