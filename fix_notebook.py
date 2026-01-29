#!/usr/bin/env python3
"""
Properly fix the broken ipynb by doing more comprehensive regex fixes
"""

import re
import json

with open('main.ipynb.backup', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Unescaped triple quotes in strings
# The file has a line like: '    """\\n",'  
# This should be: '    "\\"\\"\\"\n",' 
# The outer quotes are for JSON string, inner content is the escaped triple quotes
# Current: '    """\\n",' -> Incorrect because """ aren't escaped
# Fixed:   '    "\\"\\"\\"\n",' -> Correct: each inner quote is escaped
content = content.replace('    """\\n",', '    "\\"\\"\\"\\n",')

# Fix 2: Lines ending with [, {, (, ), }, or other chars followed by actual newline then ","
# These broken patterns: "content[\n", should be "content[\\n",
content = re.sub(r'(\[)\n",', r'\1\\n",', content)
content = re.sub(r'(\{)\n",', r'\1\\n",', content)
content = re.sub(r'(\()\n",', r'\1\\n",', content)
content = re.sub(r'(\))\n",', r'\1\\n",', content)
content = re.sub(r'(\})\n",', r'\1\\n",', content)
content = re.sub(r'(,)\n",', r'\1\\n",', content)

# Fix 3: Words at end followed by actual newline then ","
content = re.sub(r'(\w)\n",', r'\1\\n",', content)

# Fix 4: Docstring pattern - string with """[ \n]",
content = re.sub(r'"\s*\\"\\"\\"\s*\n",', r'"    \\"\\"\\"\\n",', content)

# Fix 5: Handle the case where `{{ARTICLES_JSON}}"` ends without \n and next line is ```
# This pattern: '{{ARTICLES_JSON}}",\n    "```\n",' is fine but we need to check
# Actually look for patterns where ", (on its own line) appears after string content

# Fix 6: Lines in source arrays that don't end with \n" but should
# More aggressive fix: any line inside a source array ending with just content\n followed by ",

# Fix 7: Handle the print statement with unescaped quotes
# Pattern: print("--- Generating Newsletter ---")  should have escaped quotes
# But in JSON it's: "print(\"--- Generating Newsletter ---\")"  
# The issue is: print("--- ... ---")\n",  which has literal newline
content = content.replace('print(\\"--- Generating Newsletter ---")', 
                          'print(\\"--- Generating Newsletter ---\\")')

# More general fix: any closing quote-paren followed by newline then ","
content = re.sub(r'("\))\n",', r'\1\\n",', content)

# Write the result
with open('main.ipynb', 'w', encoding='utf-8') as f:
    f.write(content)

# Validate
try:
    with open('main.ipynb', 'r', encoding='utf-8') as f:
        json.load(f)
    print("SUCCESS: Notebook is valid JSON!")
except json.JSONDecodeError as e:
    print(f"ERROR at line {e.lineno}, col {e.colno}: {e.msg}")
    with open('main.ipynb', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    start = max(0, e.lineno - 3)
    end = min(len(lines), e.lineno + 2)
    for i in range(start, end):
        marker = ">>> " if i == e.lineno - 1 else "    "
        print(f"{marker}{i+1}: {repr(lines[i][:100])}")
