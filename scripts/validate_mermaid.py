import sys
import os
import subprocess
import shutil

def extract_mermaid_blocks(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    blocks = []
    lines = content.splitlines()
    in_block = False
    current_block = []
    start_line = 0
    
    for i, line in enumerate(lines):
        if line.strip().startswith('```mermaid'):
            in_block = True
            start_line = i + 1
            current_block = []
        elif in_block and line.strip() == '```':
            in_block = False
            blocks.append({
                'content': '\n'.join(current_block),
                'start_line': start_line,
                'end_line': i + 1
            })
        elif in_block:
            current_block.append(line)
            
    return blocks

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_mermaid.py <file_path>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    blocks = extract_mermaid_blocks(file_path)
    
    if not blocks:
        print(f"No mermaid blocks found in {file_path}")
        return

    temp_dir = ".mermaid_tmp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # Save all snippets
    for i, block in enumerate(blocks):
        temp_file = os.path.join(temp_dir, f'snippet_{i}.mmd')
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(block['content'])

    print(f"Validating {len(blocks)} blocks in {file_path}...")
    
    # Run mermaid-cli on all snippets at once
    # We use a dummy output directory
    try:
        result = subprocess.run(
            ['npx', '-y', '@mermaid-js/mermaid-cli', '-i', os.path.join(temp_dir, 'snippet_*.mmd')],
            capture_output=True,
            text=True
        )
        # Note: mmdc returns 0 even if some fail? No, usually it returns non-zero if any fail.
    except Exception as e:
        print(f"Error running mermaid-cli: {e}")
        sys.exit(1)

    # The issue with mmdc is it doesn't easily map errors back to files in batch mode
    # Let's run them one by one for better reporting, but use npx cache
    
    print("\n--- MERMAID VALIDATION REPORT ---")
    all_valid = True
    for i, block in enumerate(blocks):
        temp_file = os.path.join(temp_dir, f'snippet_{i}.mmd')
        res = subprocess.run(
            ['npx', '-y', '@mermaid-js/mermaid-cli', '-i', temp_file, '-o', f'{temp_file}.svg'],
            capture_output=True,
            text=True
        )
        
        status = "✅ VALID" if res.returncode == 0 else "❌ INVALID"
        if res.returncode != 0:
            all_valid = False
            
        print(f"Block {i+1} (Lines {block['start_line']}-{block['end_line']}): {status}")
        if res.returncode != 0:
            # Extract relevant error part from stderr
            error_msg = res.stderr
            # mmdc errors can be long, let's try to find the actual message
            print(f"Error Details:\n{error_msg.strip()}")
            print("Snippet Content:")
            print(f"```mermaid\n{block['content']}\n```")
            print("-" * 40)

    if all_valid:
        print("\nAll Mermaid diagrams are valid!")
    else:
        print("\nFound errors in some Mermaid diagrams.")

    # Cleanup
    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
