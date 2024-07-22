import json

def parse_messages_from_text(text_file):
    messages = []
    with open(text_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('user:'):
                role = 'user'
                content = line[len('user:'):].strip()
            elif line.startswith('assistant:'):
                role = 'assistant'
                content = line[len('assistant:'):].strip()
            else:
                continue  # Skip lines that don't start correctly
            messages.append({'role': role, 'content': content})
    return messages

def save_to_jsonl(messages, jsonl_file):
    with open(jsonl_file, 'w', encoding='utf-8') as file:
        for message in messages:
            file.write(json.dumps(message) + '\n')  # Write each message as a new line

if __name__ == '__main__':
    text_file = 'messages/discord_messages.txt'
    jsonl_file = 'messages/discord_messages.jsonl'  # Change the extension to .jsonl
    messages = parse_messages_from_text(text_file)
    save_to_jsonl(messages, jsonl_file)
    print("Done converting text to JSONL!")
