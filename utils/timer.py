# Standard library imports
import time

# Third-party library imports

# Local imports


class Timer:
    def __init__(self):
        self.words_time = []
        self.total_time = None
        self.start_time = None
        self.word_start_time = None
        self.is_on = False

    def start_timer(self):
        self.start_time = time.time()
        self.word_start_time = time.time()
        self.is_on = True

    def next_word(self):
        self.words_time.append(time.time() - self.word_start_time)
        self.word_start_time = time.time()

    def current_time(self):
        return time.time() - self.start_time
