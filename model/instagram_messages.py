import json
import os
import re
from hidden_words import hidden_words

# Read the whole directory
def readDirectory(folder):
    return os.listdir(os.path.join(os.path.dirname(__file__), folder))

# Read the json file
def read_json_file(name):
    with open(f'{name}', encoding='utf-8') as f:
        data = json.load(f)
    return data, name

# Get the messages from the json file
def getMessages(data):
    messages = data['messages']
    return messages

def filter_messages(messages, name):
    filteredMessages = []
    # Hidden words are imported or use this
    # hidden_words = ['word1', 'word2', 'word3'] 
    for msg in messages:
        filteredMessages.append(msg)
    return filteredMessages

# Write the messages to a file in the messages folder
def writeFiles(messages, name):
    f = open(f'messages/{name}DiscordMsgs.txt', 'w', encoding='utf-8')
    for message in messages:
        f.write(message['content'])
        f.write('\n')
    f.close()
    return

def extract_relevant_data(messages, user):
    """Extracts only the relevant data (sender_name and content) from each message."""
    relevant_data = []
    for msg in messages:
        if 'sender_name' in msg and 'content' in msg:
            if msg['sender_name'] == user:
                relevant_data.append({
                    'user': msg['sender_name'],
                    'content': msg['content']
                })
            else:
                relevant_data.append({
                    'assistant': msg['sender_name'],
                    'content': msg['content']
                })
    return relevant_data


def read_directory(folder):
    return os.listdir(os.path.join(os.path.dirname(__file__), folder))

def is_message_file(filename):
    # Check if the file is a message file based on its name pattern
    return filename.startswith('message_') and filename.endswith('.json')

if __name__ == '__main__':
    instagram_user = '\u00e6\u00b1\u00aa'  # The user to filter messages for
    output_file = 'messages/instagram_messages.jsonl'

    # Process each folder within the 'Instagram' directory
    instagram_folder = read_directory('instagram')
    # Open the output file once and write filtered messages to it in JSONL format
    with open(output_file, 'w', encoding='utf-8') as file:
        for folder in instagram_folder:
            folder_path = os.path.join('instagram', folder)
            for filename in os.listdir(folder_path):
                if is_message_file(filename):  # Process only message files
                    message_file = os.path.join(folder_path, filename)
                    data = read_json_file(message_file)
                    # filtered_messages = filter_messages(data[0]['messages'], instagram_user)
                    filtered_data = extract_relevant_data(data[0]['messages'], instagram_user)
                    for message in filtered_data:
                        json_line = json.dumps(message)  # Convert dict to JSON string
                        file.write(json_line + '\n')  # Write each JSON string as a new line

    print('Done writing Instagram messages to file in JSONL format.')



    # with open(f'DMS/Linus.json', encoding='utf-8') as f:
    #     data = json.load(f)
    # messages = data['messages']
    # for msg in messages:
    #     if msg['type'] != 'Default' and msg['type'] != 'Reply':
    #         print(msg['type'])
    # print(json.dumps(messages, indent=4))
    # print(messages)
    # print(data.keys())