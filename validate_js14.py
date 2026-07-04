import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

js = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if js:
    with open('temp14.js', 'w', encoding='utf-8') as f:
        f.write(js.group(1))
