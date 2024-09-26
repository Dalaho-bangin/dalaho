import re
from core.utils import extract_js

# TODO: for map keys, javascript tolerates { param: "value" }
re_words = re.compile(r'[A-Za-z][A-Za-z0-9_]*')
re_not_junk = re.compile(r'^[A-Za-z0-9_]+$')
re_inputs = re.compile(r'''(?i)<(?:input|textarea)[^>]+?(?:id|name)=["']?([^"'\s>]+)''')
re_empty_vars = re.compile(r'''(?:[;\n]|\bvar|\blet)(\w+)\s*=\s*(?:['"`]{1,2}|true|false|null)''')
re_map_keys = re.compile(r'''['"](\w+?)['"]\s*:\s*['"`]''')

def is_not_junk(param):
    return (re_not_junk.match(param) is not None)

def heuristic(raw_response):
    potential_params = []

    headers, response = raw_response.headers, raw_response.text
    if headers.get('content-type', '').startswith(('application/json', 'text/plain')):
        if len(response) < 200:     
            potential_params = re_words.findall(response)
    # Parse Inputs
    input_names = re_inputs.findall(response)
    potential_params += input_names

    # Parse Scripts
    for script in extract_js(response):
        empty_vars = re_empty_vars.findall(script)
        potential_params += empty_vars

        map_keys = re_map_keys.findall(script)
        potential_params += map_keys

    if len(potential_params) == 0:
        return []

    found = set()
    for word in potential_params:
        if is_not_junk(word) and (word not in found):
            found.add(word)
            
    return list(found)