import time

session_start_time = None
attention_log = []  # (timestamp, score)

def start_session():
    global session_start_time
    session_start_time = time.time()

def log_attention(score):
    timestamp = time.time()
    attention_log.append((timestamp, score))

def get_session_data():
    return session_start_time, time.time(), attention_log
