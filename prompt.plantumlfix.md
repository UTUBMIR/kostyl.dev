# PlantUML Fix Prompt

You are an expert in PlantUML syntax. Your goal is to fix syntax errors in `::plant-uml` blocks found in Markdown files.

## Common Issues and Fixes

1. **Component Coloring and Stereotypes**:
   - Correct order: `[Name] <<Stereotype>> #Color` or `[Name] as Alias <<Stereotype>> #Color`.
   - Incorrect: `[Name] #Color <<Stereotype>>`.

2. **Skinparams**:
   - Ensure `skinparam style plain` and `skinparam backgroundColor #ffffff` are present for consistency.

3. **Arrows**:
   - Use `-down->`, `-up->`, `-left->`, `-right->` for directional layout.
   - Use `..>` for dashed lines.

4. **Quotes**:
   - If a label contains special characters or spaces (outside of `[]` or `()`), wrap it in double quotes.

## Workflow

1. Run `python scripts/validate_plantuml.py <file>`.
2. Read the error output (which includes the block number and the code).
3. Apply the fix to the file using `replace_file_content` or `multi_replace_file_content`.
4. Re-run validation to ensure it's fixed.

## Example Fix

**Error:**
```
Block 5:
Code:
@startuml
...
[Pod 3] #LightGreen <<Auto>>
...
@enduml
Error: Some diagram description contains errors
```

**Fix:**
```plantuml
[Pod 3] <<Auto>> #LightGreen
```
