import Constants

def log(msg):
    if Constants.LOGGING_ENABLED:
        with open(Constants.LOGGING_FILE, 'a', encoding='utf-8') as f:
            f.write(str(msg) + '\n')


def clear_log():
    if Constants.LOGGING_ENABLED:
        with open(Constants.LOGGING_FILE, 'w', encoding='utf-8') as f:
            f.write('')  # Clear the file by writing an empty string