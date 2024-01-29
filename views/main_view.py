# Standard library imports
import os
import time
from itertools import zip_longest
from tkinter import StringVar, IntVar
from threading import Thread

# Third-party library imports
from customtkinter import CTkFrame, CTkLabel, CTkImage, CTkEntry
from PIL import Image


# Local imports
from utils import SUBTITLE_FONT, TITLE_FONT, TEXT_FONT, SCREEN_SCALE, WORD_PAD, Timer


class MainView(CTkFrame):
    def __init__(self, parent, switch_view, *args, **kwargs):
        CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.switch_view = switch_view

        self.words_list = [
            "pound",
            "language",
            "don't",
            "use",
            "may",
            "hear",
            "hand",
            "ago",
            "girl",
            "hot",
            "mark",
            "record",
            "is",
            "change",
            "reach",
            "under",
            "close",
            "wheel",
            "pool",
            "shore",
            "door",
            "rocket",
            "mountain",
            "cat",
            "dog",
            "pound",
            "language",
            "don't",
            "use",
            "may",
            "hear",
            "hand",
            "ago",
            "girl",
            "hot",
            "mark",
            "record",
            "is",
            "change",
            "reach",
            "under",
            "close",
            "wheel",
            "pool",
            "shore",
            "door",
            "rocket",
            "mountain",
            "cat",
            "dog",
            "pound",
            "language",
            "don't",
            "use",
            "may",
            "hear",
            "hand",
            "ago",
            "girl",
            "hot",
            "mark",
            "record",
            "is",
            "change",
            "reach",
            "under",
            "close",
            "wheel",
            "pool",
            "shore",
            "door",
            "rocket",
            "mountain",
            "cat",
            "dog",
            "pound",
            "language",
            "don't",
            "use",
            "may",
            "hear",
            "hand",
            "ago",
            "girl",
            "hot",
            "mark",
            "record",
            "is",
            "change",
            "reach",
            "under",
            "close",
            "wheel",
            "pool",
            "shore",
            "door",
            "rocket",
            "mountain",
            "cat",
            "dog",
        ]
        self.current_word_index = 0
        self.active_word_index = 0

        self.words_results = []

        self.word_height = None
        self.cumulative_width = WORD_PAD
        self.cumulative_height = WORD_PAD

        # initialize Title
        self.initialize_titles()

        # Initialize timers
        self.initialize_timers()

        # Initialize Canvas
        self.initialize_canvas()

        # Initialize Entry
        self.initialize_entry()
        self.entry.focus()

        self.timer = Timer()

        self.bind("<Configure>", self.configure_event_handler)
        self.entry_text.trace_add("write", self.entry_text_callback)

    def initialize_titles(self):
        self.titles_frame = CTkFrame(self, fg_color="transparent")
        self.titles_frame.pack(pady=50)

        # Create logo on both side of the text
        logo_image_path = os.path.join("resources", "images", "logo.png")
        pil_logo_image = Image.open(logo_image_path)
        self.logo_image = CTkImage(pil_logo_image, size=(150, 150))
        self.logo_image_label1 = CTkLabel(
            self.titles_frame, image=self.logo_image, text=None
        )
        self.logo_image_label2 = CTkLabel(
            self.titles_frame, image=self.logo_image, text=None
        )
        self.logo_image_label1.pack(side="right")
        self.logo_image_label2.pack(side="left")

        # Create Title and SubTitle
        self.subtitle = CTkLabel(
            self.titles_frame, text="Typing Speed Test", font=SUBTITLE_FONT
        )
        self.subtitle.pack()
        self.title = CTkLabel(
            self.titles_frame, text="Test your typing ability", font=TITLE_FONT
        )
        self.title.pack()

    def initialize_timers(self):
        self.timers_frame = CTkFrame(self, fg_color="transparent")
        self.timers_frame.pack()

        self.time_left = IntVar(value=60)
        self.time_left_frame = CTkFrame(self.timers_frame)
        self.time_left_frame.pack(side="right", padx=50)
        self.time_left_label = CTkLabel(self.time_left_frame, text="Time Left: ")
        self.time_left_value = CTkLabel(
            self.time_left_frame, textvariable=self.time_left
        )

        self.time_left_label.pack(side="left")
        self.time_left_value.pack(side="right")

        self.wpm = IntVar()
        self.wpm_frame = CTkFrame(self.timers_frame)
        self.wpm_frame.pack(side="left", padx=50)
        self.wpm_label = CTkLabel(self.wpm_frame, text="WPM: ")
        self.wpm_value = CTkLabel(self.wpm_frame, textvariable=self.wpm)

        self.wpm_label.pack(side="left")
        self.wpm_value.pack(side="right")

        self.cpm = IntVar()
        self.cpm_frame = CTkFrame(self.timers_frame)
        self.cpm_frame.pack(side="left", padx=50)
        self.cpm_label = CTkLabel(self.cpm_frame, text="CPM: ")
        self.cpm_value = CTkLabel(self.cpm_frame, textvariable=self.cpm)

        self.cpm_label.pack(side="left")
        self.cpm_value.pack(side="right")

    def initialize_canvas(self):
        self.parent.update_idletasks()
        pad_x = self.parent.winfo_screenwidth() * SCREEN_SCALE * 0.1
        self.canvas_w = 8 * pad_x
        self.canvas = CTkFrame(self)
        self.canvas.pack(fill="x", padx=pad_x)

        self.create_word_frame()
        self.set_active_word()
        self.canvas_h = self.word_height * 3 + WORD_PAD * 4
        self.canvas.configure(height=self.canvas_h)

    def initialize_entry(self):
        self.entry_text = StringVar()
        self.entry = CTkEntry(self, textvariable=self.entry_text)
        self.entry.pack()

    def create_word_frame(self):
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
        self.canvas.update_idletasks()
        self.update_words_layout()
        while self.cumulative_height < 3 * self.word_height + 4 * WORD_PAD:
            self.create_word_frame()

    def place_word_frame(self, word_frame):
        word_width = word_frame.winfo_reqwidth() * SCREEN_SCALE

        # Check if adding the next word would exceed the available width
        if self.cumulative_width + word_width + WORD_PAD > self.canvas_w:
            self.cumulative_width = WORD_PAD  # Reset cumulative width for the new row
            self.cumulative_height += self.word_height + WORD_PAD

        word_frame.place(x=self.cumulative_width, y=self.cumulative_height, anchor="nw")

        self.cumulative_width += word_width + WORD_PAD

    def update_words_layout(self):
        self.canvas_w = self.canvas.winfo_width() * SCREEN_SCALE

        self.cumulative_width = WORD_PAD
        self.cumulative_height = WORD_PAD
        for word_frame in self.canvas.winfo_children():
            self.place_word_frame(word_frame)

    def scroll_lines(self):
        iterations = 6

        # Incremental movement in pixels per iteration
        total_movement = self.word_height + WORD_PAD
        movement_per_iteration = (total_movement) / iterations

        for word_frame in self.canvas.winfo_children():
            current_y = word_frame.winfo_y() * SCREEN_SCALE
            current_x = word_frame.winfo_x() * SCREEN_SCALE
            target_y = current_y - self.word_height - WORD_PAD
            # Start the smooth animation
            self.move_word_frame_smoothly(
                word_frame,
                current_x,
                current_y,
                target_y,
                iterations,
                movement_per_iteration,
            )

        self.cumulative_height -= total_movement
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
        if iteration > 0:
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

    def entry_text_callback(self, var=None, index=None, mode=None):
        if not self.timer.is_on:
            self.timer.start_timer()
            self.after(1000, self.start_countdown)

        word_frame = self.canvas.winfo_children()[self.active_word_index]
        word_entered = self.entry_text.get()

        if word_entered != "" and word_entered[-1] == " ":
            self.check_final_word()
            self.next_word()
            self.check_scroll()
        else:
            for letter_frame, input_letter in zip_longest(
                word_frame.winfo_children(), word_entered
            ):
                if letter_frame is not None:
                    letter = letter_frame.cget("text")
                    if input_letter == letter:
                        letter_frame.configure(text_color="blue")
                    elif input_letter is None:
                        letter_frame.configure(text_color="black")
                    else:
                        letter_frame.configure(text_color="red")

    def set_active_word(self):
        word_frame = self.canvas.winfo_children()[self.active_word_index]
        word_frame.configure(fg_color="#96E9C6")

    def next_word(self):
        self.timer.next_word()

        word_frame = self.canvas.winfo_children()[self.active_word_index]
        word_frame.configure(fg_color="transparent")
        self.active_word_index += 1
        self.entry.delete(0, "end")
        self.set_active_word()

    def check_scroll(self):
        word_frame = self.canvas.winfo_children()[self.active_word_index]

        if (word_frame.winfo_y() * SCREEN_SCALE) > (
            3 * WORD_PAD + 2 * self.word_height
        ):
            scroll_thread = Thread(target=self.scroll_lines)
            scroll_thread.start()
            for word_frame in self.canvas.winfo_children():
                if word_frame.winfo_y() * SCREEN_SCALE < 0:
                    word_frame.destroy()
                    self.active_word_index -= 1
                else:
                    break
            while self.cumulative_height < 3 * self.word_height + 4 * WORD_PAD:
                self.create_word_frame()

    def check_final_word(self):
        word_frame = self.canvas.winfo_children()[self.active_word_index]
        word_entered = self.entry_text.get()[:-1]
        is_correct = True
        for letter_frame, input_letter in zip_longest(
            word_frame.winfo_children(), word_entered
        ):
            if letter_frame is None:
                is_correct = False
                break
            else:
                letter = letter_frame.cget("text")
                if input_letter != letter:
                    is_correct = False
                    break
        result = {
            "is_correct": is_correct,
            "word": self.words_list[self.active_word_index],
            "word_time": (self.timer.current_time() - self.timer.word_start_time) / 60,
        }
        self.words_results.append(result)
        self.set_cpm_wpm()
        if is_correct:
            text_color = "blue"
        else:
            text_color = "red"
        for letter_frame in word_frame.winfo_children():
            letter_frame.configure(text_color=text_color)
        word_frame.configure(fg_color="transparent")

    def set_cpm_wpm(self):
        char_count = 0
        words_count = 0
        total_minute = self.timer.current_time() / 60
        for result in self.words_results:
            if result["is_correct"]:
                char_count += len(result["word"])
                words_count += 1
        if words_count == 0:
            mean_cpm = 0
        else:
            mean_cpm = int(char_count / total_minute)
        mean_wpm = int(words_count / total_minute)
        self.cpm.set(mean_cpm)
        self.wpm.set(mean_wpm)

    def start_countdown(self):
        time_left = self.time_left.get()
        self.time_left.set(time_left - 1)
        if time_left > 1:
            self.after(1000, self.start_countdown)
        else:
            self.entry.configure(state="disabled")
