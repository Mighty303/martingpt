import json
import os
import re
from hidden_words import hidden_words

def read_directory(folder):
    return os.listdir(os.path.join(os.path.dirname(__file__), folder))

def read_json_file(folder, name):
    with open(f'{folder}/{name}.json', encoding='utf-8') as f:
        data = json.load(f)
    return data, name

def get_messages(data):
    return data['messages']

def filter_sensitive_data(messages):
    # Regex for detecting emails and U.S. phone numbers
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_regex = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    
    # Replace detected patterns with generic placeholders
    messages = re.sub(email_regex, '[EMAIL]', messages)
    messages = re.sub(phone_regex, '[PHONE]', messages)
    return messages

def filter_messages(messages, user):
    filtered_msgs = []
    last_msg = None
    for msg in messages:
        msg['content'] = filter_sensitive_data(msg['content'])
        if msg['content'].strip() == '' or msg['attachments'] != [] or re.search(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.[a-zA-Z]{2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*', msg['content']):
            continue
        if msg['type'] not in ['Default'] or any(word in msg['content'].lower() for word in hidden_words):
            continue
        role = 'user' if msg['author']['name'] == user else 'assistant'
        if last_msg and last_msg['role'] != role:
            # Assuming 'user' is 'assistant' and vice versa for the prompt and completion
            if last_msg['role'] == 'assistant':
                filtered_msgs.append({'prompt': last_msg['content'], 'completion': msg['content']})
        last_msg = {'role': role, 'content': msg['content']}
    return filtered_msgs



def write_to_jsonl(messages, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for message in messages:
            json.dump(message, f)
            f.write('\n')

if __name__ == '__main__':
    discord_user = 'mighty._'
    discord_files = read_directory('discord')
    output_file = 'messages/training_data.jsonl'  # Output JSONL file for training data

    all_messages = []
    for file in discord_files:
        file = file.replace('.json', '')
        data, _ = read_json_file('discord', file)
        messages = get_messages(data)
        filtered_messages = filter_messages(messages, discord_user)
        all_messages.extend(filtered_messages)

    write_to_jsonl(all_messages, output_file)
    print('Done generating JSONL file!')
