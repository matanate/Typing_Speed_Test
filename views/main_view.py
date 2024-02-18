# Standard library imports
import os
import csv
from itertools import zip_longest
from tkinter import StringVar, IntVar
from threading import Thread
import random

# Third-party library imports
from customtkinter import CTkFrame, CTkLabel, CTkEntry


# Local imports
from utils import TEXT_FONT, SCREEN_SCALE, WORD_PAD, TIMERS_FONT, Timer


class MainView(CTkFrame):
    """
    MainView class represents the main view of the typing speed test application.

    Attributes:
        parent (Tk): The parent Tkinter window.
        switch_view (function): Function to switch to a different view.
        words_list (list): List of words to be typed in the test.
        current_word_index (int): Index of the current word in the words_list.
        active_word_index (int): Index of the word currently active for typing.
        words_results (list): List to store results for each word typed.
        word_height (float): Height of a word frame in pixels.
        cumulative_width (float): Cumulative width of word frames in the canvas.
        cumulative_height (float): Cumulative height of word frames in the canvas.
        timer (Timer): Timer object for tracking time during the typing test.
    """

    def __init__(self, parent, switch_view, *args, **kwargs):
        """
        Initialize the MainView.

        Args:
            parent (Tk): The parent Tkinter window.
            switch_view (function): Function to switch to a different view.
            *args, **kwargs: Additional arguments for CTkFrame initialization.
        """
        CTkFrame.__init__(self, parent, *args, **kwargs)
        self.configure(fg_color="transparent")
        self.parent = parent
        self.switch_view = switch_view

        # Load words from a CSV file
        with open(os.path.join("resources", "data", "Words.csv")) as file:
            file_list = list(csv.reader(file))
        self.words_list = [word[0].lower() for word in file_list]
        random.shuffle(self.words_list)

        # Initialize word indices and result list
        self.current_word_index = 0
        self.active_word_index = 0
        self.words_results = []

        # Initialize word frame dimensions
        self.word_height = None
        self.cumulative_width = WORD_PAD
        self.cumulative_height = WORD_PAD

        # Initialize timers
        self.initialize_timers()

        # Initialize Canvas
        self.initialize_canvas()

        # Initialize Entry
        self.initialize_entry()
        self.entry.focus()

        # Initialize Timer object
        self.timer = Timer()

        # Bind canvas configuration event and entry text callback
        self.bind("<Configure>", self.configure_event_handler)
        self.entry_text.trace_add("write", self.entry_text_callback)

    def initialize_timers(self):
        """
        Initialize the timers frame, time_left, wpm, and cpm labels.
        """
        # Create timers frame
        self.timers_frame = CTkFrame(self, fg_color="transparent")
        self.timers_frame.pack()

        # Initialize time_left label and variable
        self.time_left = IntVar(value=60)
        self.time_left_frame = CTkFrame(self.timers_frame, fg_color="transparent")
        self.time_left_frame.pack(side="right", padx=50)
        self.time_left_label = CTkLabel(
            self.time_left_frame, text="Time Left: ", font=TIMERS_FONT + ("bold",)
        )
        self.time_left_value = CTkLabel(
            self.time_left_frame, textvariable=self.time_left, font=TIMERS_FONT
        )

        # Pack time_left label and value
        self.time_left_label.pack(side="left")
        self.time_left_value.pack(side="right")

        # Initialize wpm label and variable
        self.wpm = IntVar()
        self.wpm_frame = CTkFrame(self.timers_frame, fg_color="transparent")
        self.wpm_frame.pack(side="left", padx=50)
        self.wpm_label = CTkLabel(
            self.wpm_frame, text="WPM: ", font=TIMERS_FONT + ("bold",)
        )
        self.wpm_value = CTkLabel(
            self.wpm_frame, textvariable=self.wpm, font=TIMERS_FONT
        )

        # Pack wpm label and value
        self.wpm_label.pack(side="left")
        self.wpm_value.pack(side="right")

        # Initialize cpm label and variable
        self.cpm = IntVar()
        self.cpm_frame = CTkFrame(self.timers_frame, fg_color="transparent")
        self.cpm_frame.pack(side="left", padx=50)
        self.cpm_label = CTkLabel(
            self.cpm_frame, text="CPM: ", font=TIMERS_FONT + ("bold",)
        )
        self.cpm_value = CTkLabel(
            self.cpm_frame, textvariable=self.cpm, font=TIMERS_FONT
        )
        # Pack cpm label and value
        self.cpm_label.pack(side="left")
        self.cpm_value.pack(side="right")

    def initialize_canvas(self):
        """
        Initialize the canvas for displaying words and start the canvas layout.
        """
        self.parent.update_idletasks()
        pad_x = self.parent.winfo_screenwidth() * SCREEN_SCALE * 0.1
        self.canvas_w = 8 * pad_x
        # Initialize canvas Frame
        self.canvas = CTkFrame(self)
        self.canvas.pack(fill="x", padx=pad_x)

        # Initialize first word frame to calculate word hight
        self.create_word_frame()
        self.set_active_word()
        self.canvas_h = self.word_height * 3 + WORD_PAD * 4

        # Set canvas hight
        self.canvas.configure(height=self.canvas_h)

    def initialize_entry(self):
        """
        Initialize the entry widget for user input.
        """
        self.entry_text = StringVar()
        self.entry = CTkEntry(self, textvariable=self.entry_text)
        self.entry.pack()

    def create_word_frame(self):
        """
        Create a frame for displaying a word and add it to the canvas.
        """
        word_frame = CTkFrame(self.canvas, fg_color="transparent")
        word = self.words_list[self.current_word_index]
        self.current_word_index += 1
        for letter in word:
            letter_label = CTkLabel(word_frame, text=letter, font=TEXT_FONT)
            letter_label.pack(side="left")
        self.canvas.update_idletasks()
        if not self.word_height:
            self.word_height = word_frame.winfo_reqheight() * SCREEN_SCALE
        self.place_word_frame(word_frame)

    def configure_event_handler(self, event=None):
        """
        Handle the canvas configuration event.

        Args:
            event: The event object (default is None).
        """
        self.canvas.update_idletasks()
        self.update_words_layout()
        while self.cumulative_height <= 3 * self.word_height + 4 * WORD_PAD:
            self.create_word_frame()

    def place_word_frame(self, word_frame):
        """
        Place a word frame on the canvas.

        Args:
            word_frame: The word frame to be placed on the canvas.
        """
        word_width = word_frame.winfo_reqwidth() * SCREEN_SCALE

        # Check if adding the next word would exceed the available width
        if self.cumulative_width + word_width + WORD_PAD > self.canvas_w:
            self.cumulative_width = WORD_PAD  # Reset cumulative width for the new row
            self.cumulative_height += self.word_height + WORD_PAD

        # Place the word frame on the canvas
        word_frame.place(x=self.cumulative_width, y=self.cumulative_height, anchor="nw")

        # Move to next word location
        self.cumulative_width += word_width + WORD_PAD

    def update_words_layout(self):
        """
        Update the layout of word frames in the canvas.
        """
        self.canvas_w = self.canvas.winfo_width() * SCREEN_SCALE
        self.cumulative_width = WORD_PAD
        self.cumulative_height = WORD_PAD
        # Check if adding the next word would exceed the available width and if so place a new word
        for word_frame in self.canvas.winfo_children():
            self.place_word_frame(word_frame)

    def entry_text_callback(self, var=None, index=None, mode=None):
        """
        Handle the callback when there is a change in the entry text.

        Args:
            var: The StringVar object (default is None).
            index: The index value (default is None).
            mode: The mode value (default is None).
        """
        # Start timer and countdown if it is not already on
        if not self.timer.is_on:
            self.timer.start_timer()
            self.after(1000, self.start_countdown)

        # Get current word frame and word entered
        word_frame = self.canvas.winfo_children()[self.active_word_index]
        word_entered = self.entry_text.get()

        # Check for a " " to move to next word
        if word_entered != "" and word_entered[-1] == " ":
            self.check_final_word(word_frame)
            self.next_word()
            word_frame = self.canvas.winfo_children()[self.active_word_index]
            self.check_scroll(word_frame)

            # Destroy the line that was scrolled
            for word_frame in self.canvas.winfo_children():
                if word_frame.winfo_y() * SCREEN_SCALE < 0:
                    word_frame.destroy()
                    self.active_word_index -= 1
                else:
                    # Break out of the loop if the word is on the screen
                    break
        else:
            # Loop through each letter in the entered word and check its validity
            for letter_frame, input_letter in zip_longest(
                word_frame.winfo_children(), word_entered
            ):
                if letter_frame is not None:
                    letter = letter_frame.cget("text")
                    if input_letter == letter:
                        # Highlight the correct letter
                        letter_frame.configure(text_color="blue")
                    elif input_letter is None:
                        # Unhighlight letters that was not entered
                        letter_frame.configure(text_color="black")
                    else:
                        # Highlight the incorrect letter
                        letter_frame.configure(text_color="red")

    def set_active_word(self):
        """
        Set the active word frame by highlighting it.
        """
        word_frame = self.canvas.winfo_children()[self.active_word_index]
        word_frame.configure(fg_color="#96E9C6")

    def next_word(self):
        """
        Move to the next word in the test.
        """
        self.timer.next_word()

        # UnHighlight the current word frame
        word_frame = self.canvas.winfo_children()[self.active_word_index]
        word_frame.configure(fg_color="transparent")
        self.active_word_index += 1

        # Clear the entry
        self.entry.delete(0, "end")
        self.set_active_word()

    def check_scroll(self, word_frame):
        """
        Check if scrolling of the canvas is required and initiate the scroll if needed.

        Args:
        word_frame (tkinter.Frame): The current word frame.
        """
        # Check if scrolling is required (active word in third row)
        if (word_frame.winfo_y() * SCREEN_SCALE) >= (
            3 * WORD_PAD + 2 * self.word_height
        ):
            # Scroll the current lines on the canvas in a thread
            frames_list = [word_frame for word_frame in self.canvas.winfo_children()]
            scroll_thread = Thread(target=self.scroll_lines, args=(frames_list,))
            scroll_thread.start()

            # Readjust the cumulative height
            self.cumulative_height -= self.word_height + WORD_PAD

            # Check if there are word missing in the 4th row, Add words until the row is full
            while self.cumulative_height <= 3 * self.word_height + 4 * WORD_PAD:
                self.create_word_frame()

    def scroll_lines(self, frames_list):
        """
        Smoothly scroll the lines of the canvas.

        Args:
            frames_list: List of word frames to be scrolled.
        """
        iterations = 6

        # Incremental movement in pixels per iteration
        total_movement = self.word_height + WORD_PAD
        movement_per_iteration = (total_movement) / iterations

        # Loop through each word frame
        for word_frame in frames_list:
            # Get the current x and y coordinates of the word frame
            current_y = word_frame.winfo_y() * SCREEN_SCALE
            current_x = word_frame.winfo_x() * SCREEN_SCALE
            target_y = current_y - self.word_height - WORD_PAD
            # Start the scroll animation
            self.move_word_frame_smoothly(
                word_frame,
                current_x,
                current_y,
                target_y,
                iterations,
                movement_per_iteration,
            )

        # update the canvas
        self.canvas.update()

    def move_word_frame_smoothly(
        self,
        word_frame,
        current_x,
        current_y,
        target_y,
        iteration,
        movement_per_iteration,
    ):
        """
        Move a word frame smoothly during scrolling.

        Args:
            word_frame: The word frame to be moved.
            current_x: The current x-coordinate of the word frame.
            current_y: The current y-coordinate of the word frame.
            target_y: The target y-coordinate for the word frame.
            iteration: The current iteration count.
            movement_per_iteration: The movement per iteration in pixels.
        """
        # Check if iterations are over
        if iteration > 0:
            # Place the word upward
            new_y = current_y - movement_per_iteration
            word_frame.place(x=current_x, y=new_y)

            # Schedule the next movement
            self.after(
                1,
                self.move_word_frame_smoothly,
                word_frame,
                current_x,
                new_y,
                target_y,
                iteration - 1,
                movement_per_iteration,
            )

    def check_final_word(self, word_frame):
        """
        Check and process the correctness of the final word typed by the user.

        Args:
        word_frame (tkinter.Frame): The current word frame.
        """
        # Get the word entered by the user (without the last space)
        word_entered = self.entry_text.get()[:-1]
        is_correct = True

        # Loop through each letter in the entered word and check its validity
        for letter_frame, input_letter in zip_longest(
            word_frame.winfo_children(), word_entered
        ):
            # Check if the letter is None (word entered is longer then than the word)
            if letter_frame is None:
                is_correct = False
                break
            else:
                # Get the current letter
                letter = letter_frame.cget("text")
                # Check if the letter entered is correct
                if input_letter != letter:
                    is_correct = False
                    break
        # Save the word result and append it to the words_results list
        result = {
            "is_correct": is_correct,
            "word": self.words_list[self.active_word_index],
            "word_entered": word_entered,
        }
        self.words_results.append(result)

        # Update the CPM and WPM values
        self.set_cpm_wpm()

        # Check if the word is correct and highlight Blue/Red
        if is_correct:
            text_color = "blue"
        else:
            text_color = "red"
        for letter_frame in word_frame.winfo_children():
            letter_frame.configure(text_color=text_color)

        # UnHighlight the current word frame
        word_frame.configure(fg_color="transparent")

    def set_cpm_wpm(self):
        """
        Calculate and set the CPM and WPM values based on user input.
        """
        char_count = 0
        words_count = 0

        # Get the total time passed in minutes
        total_minute = self.timer.current_time() / 60

        # Count correct characters and words
        for result in self.words_results:
            if result["is_correct"]:
                char_count += len(result["word"])
                words_count += 1

        # Prevent division by zero
        if words_count == 0:
            mean_cpm = 0
        else:
            # Calculate the mean CPM
            mean_cpm = int(char_count / total_minute)

        # Calculate the current mean WPM
        mean_wpm = int(words_count / total_minute)

        # Set the CPM and WPM values
        self.cpm.set(mean_cpm)
        self.wpm.set(mean_wpm)

    def start_countdown(self):
        """
        Start the countdown timer for the typing test.
        """
        time_left = self.time_left.get()
        self.time_left.set(time_left - 1)

        # Recursive call the function every 1 second
        if time_left > 1:
            self.after(1000, self.start_countdown)
        else:
            # Change view to the result view when the countdown is over
            self.switch_view(self.parent.ResultView, self.words_results)
