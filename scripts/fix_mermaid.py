import re
import os
import sys

def fix_block(match):
    block = match.group(1)
    if 'sequenceDiagram' in block:
        lines = block.splitlines()
        new_lines = []
        for line in lines:
            if not line.strip().startswith('style '):
                # Simple quote enforcement for labels
                if '->' in line and ':' in line:
                    parts = line.split(':', 1)
                    label = parts[1].strip()
                    if not (label.startswith('"') and label.endswith('"')):
                        line = f'{parts[0]}: "{label}"'
                new_lines.append(line)
        return '```mermaid\n' + '\n'.join(new_lines) + '\n```'
    return match.group(0)

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_mermaid.py <file.md>")
        return
    
    file_path = sys.argv[1]
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = re.sub(r'```mermaid\n(.*?)\n```', fix_block, content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed mermaid blocks.")

if __name__ == "__main__":
    main()
