import re

def unwrap_svg(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    def replacer(match):
        return match.group(1)

    new_content = re.sub(r'<div class="w-full block">\n(<svg viewBox=.*?</svg>)\n</div>', replacer, content, flags=re.DOTALL)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {file_path}")
    else:
        print(f"No changes for {file_path}")

files = [
    '/Users/arakviel/Work/kostyl.dev/content/07.tools/01.docker/01.containerization-concept.md',
    '/Users/arakviel/Work/kostyl.dev/content/07.tools/01.docker/02.docker-what-and-why.md',
    '/Users/arakviel/Work/kostyl.dev/content/98.test-new-components.md'
]

for file_path in files:
    unwrap_svg(file_path)

