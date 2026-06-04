import os

file_path = 'content/13.aws/09.dynamodb.md'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the start and end of the block we want to remove
start_marker = "---Projection = [Amazon.DynamoDBv2.Model.Projection]@{"
end_marker = "::\n\n## Частина 4: DynamoDB Streams та Транзакції"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    # We want to keep the ending part: "\n\n## Частина 4: DynamoDB Streams та Транзакції"
    # So we replace from start_idx to end_idx + len("::")
    to_remove = content[start_idx : end_idx + len("::")]
    print("Found block to remove. Length:", len(to_remove))
    new_content = content[:start_idx] + content[end_idx + len("::"):]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully removed the corrupted block!")
else:
    print("Markers not found!")
    print("start_idx:", start_idx)
    print("end_idx:", end_idx)
