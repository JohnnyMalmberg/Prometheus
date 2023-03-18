import os

def next_chat_log_file():
    index = 0
    while os.path.exists(f'data/chat_logs/log_{index}.chat'):
        index += 1
    return f'data/chat_logs/log_{index}.chat'

def log_chat(file_name, messages):
    with open(file_name, 'a') as log:
        def extract(message):
            return (message['role'], message['content'])
        extracted_messages = [extract(m) for m in messages]
        lines = [f'{a}:\n{b}' for (a,b) in extracted_messages]
        joined_lines = "\n".join(lines)
        log_content = f'{"="*50} ChatCompletion {"="*50}\n\n{joined_lines}\n\n'
        log.write(log_content)