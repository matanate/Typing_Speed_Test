# Standard library imports
import time

# Third-party library imports

# Local imports


class Timer:
    """
    Timer class provides functionality for measuring time intervals.

    Attributes:
        words_time (list): List to store individual word completion times.
        total_time (float or None): Total time elapsed since the timer started. Initialized to None.
        start_time (float or None): Start time of the timer. Initialized to None.
        word_start_time (float or None): Start time of the current word. Initialized to None.
        is_on (bool): Flag to indicate whether the timer is running or paused. Initialized to False.
    """

    def __init__(self):
        """
        Initialize the Timer object.
        """
        self.words_time = []
        self.total_time = None
        self.start_time = None
        self.word_start_time = None
        self.is_on = False

    def start_timer(self):
        """
        Start the timer.
        """
        self.start_time = time.time()
        self.word_start_time = time.time()
        self.is_on = True

    def next_word(self):
        """
        Record the time for the completion of the current word and reset the word start time.
        """
        self.words_time.append(time.time() - self.word_start_time)
        self.word_start_time = time.time()

    def current_time(self):
        """
        Get the total elapsed time since the timer started.
        """
        return time.time() - self.start_time
