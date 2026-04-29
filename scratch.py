import re

with open('/Users/arakviel/Work/kostyl.dev/content/12.html-css/05.html-forms.md', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to find ```html blocks that are NOT already preceded by ::html-preview
# We'll split the text and iterate.

lines = content.split('\n')
new_lines = []

i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith('```html'):
        # Check if previous non-empty line is ::html-preview
        prev_idx = i - 1
        is_already_wrapped = False
        while prev_idx >= 0 and lines[prev_idx].strip() == '':
            prev_idx -= 1
        if prev_idx >= 0 and lines[prev_idx].strip() == '::html-preview':
            is_already_wrapped = True
        
        if is_already_wrapped:
            new_lines.append(line)
            i += 1
            continue
        
        # Not wrapped, let's wrap it!
        new_lines.append('::html-preview')
        new_lines.append('')
        new_lines.append(line)
        
        # Find closing ```
        i += 1
        while i < len(lines):
            close_line = lines[i]
            new_lines.append(close_line)
            if close_line.startswith('```'):
                # Check if there is already a `::` closing tag?
                # Sometimes there's CSS block after HTML block. If we wrap only HTML, we must close after HTML.
                # Let's peek ahead to see if there is ```css.
                # Actually, no, if it's already wrapped, the script skips it. 
                # If it's NOT wrapped, we just wrap the HTML block.
                # Wait, if there's no ```css, we wrap it.
                break
            i += 1
        
        new_lines.append('')
        new_lines.append('::')
    else:
        new_lines.append(line)
    i += 1

with open('/Users/arakviel/Work/kostyl.dev/content/12.html-css/05.html-forms.md.tmp', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print("Done")
