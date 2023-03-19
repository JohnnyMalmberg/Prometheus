from threading import Lock
import time

import openai

from core.log import *

model = 'gpt-3.5-turbo'

tokens_per_second = 20

spent_tokens = 0
token_allowance = 1000
last_api_call = time.time()
lock = Lock()

log_file = next_chat_log_file()

def gpt_message(role, content):
    return [{'role':role,'content':content}]

def simple_chat(messages, temperature=1.2, n=1, **kwargs):
    lock.acquire()
    global token_allowance
    global last_api_call
    global spent_tokens
    current_time = time.time()
    extra_tokens = (int) ((current_time - last_api_call) * tokens_per_second)
    unspent_allowance = (token_allowance + extra_tokens) - spent_tokens

    while unspent_allowance < 0:
        waiting_period = -(unspent_allowance / tokens_per_second)
        print(f'Waiting {waiting_period} seconds for {-unspent_allowance} tokens.')
        time.sleep(waiting_period)
        current_time = time.time()
        extra_tokens = (int) ((current_time - last_api_call) * tokens_per_second)
        unspent_allowance = (token_allowance + extra_tokens) - spent_tokens

    token_allowance += extra_tokens
    last_api_call = current_time

    try:
        comp = openai.ChatCompletion.create(model=model, messages=messages, temperature=temperature, n=n, **kwargs)
        spent_tokens += comp['usage']['total_tokens']
    except Exception as e:
        print(f'Failure in openai chatcompletion: {e}')
    finally:
        print(f'Tokens: {spent_tokens} spent / {token_allowance} allowed')
        lock.release()

    response = [comp['choices'][x]['message']['content'].strip() for x in range(n)]

    messages_final = messages + [gpt_message('assistant', r)[0] for r in response]
    log_chat(log_file, messages_final)

    return response[0] if n == 1 else response

