# Standard library imports
import os
from itertools import zip_longest
from tkinter import StringVar

# Third-party library imports
from customtkinter import CTkFrame, CTkLabel, CTkImage, CTkEntry
from PIL import Image


# Local imports
from utils import SUBTITLE_FONT, TITLE_FONT, TEXT_FONT, SCREEN_SCALE, WORD_PAD


class MainView(CTkFrame):
    def __init__(self, parent, switch_view, *args, **kwargs):
        CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.switch_view = switch_view

        self.words_set = [
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

        self.word_height = None
        self.cumulative_width = WORD_PAD
        self.cumulative_height = WORD_PAD

        # initialize Title
        self.initialize_titles()

        # Initialize Canvas
        self.initialize_canvas()

        # Initialize Entry
        self.initialize_entry()

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

    def initialize_canvas(self):
        self.parent.update_idletasks()
        pad_x = self.parent.winfo_screenwidth() * SCREEN_SCALE * 0.1
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
        word_label = CTkFrame(self.canvas, fg_color="transparent")
        word = self.words_set[self.current_word_index]
        self.current_word_index += 1
        for letter in word:
            letter_label = CTkLabel(word_label, text=letter, font=TEXT_FONT)
            letter_label.pack(side="left")
        self.canvas.update_idletasks()
        if not self.word_height:
            self.word_height = word_label.winfo_reqheight() * SCREEN_SCALE

    def configure_event_handler(self, event=None):
        while self.cumulative_height < 3 * self.word_height + 4 * WORD_PAD:
            self.create_word_frame()
            self.update_words_layout()
        self.update_words_layout()

    def update_words_layout(self):
        self.canvas.update_idletasks()
        self.canvas_w = self.canvas.winfo_width() * SCREEN_SCALE

        self.cumulative_width = WORD_PAD
        self.cumulative_height = WORD_PAD

        for word_frame in self.canvas.winfo_children():
            word_width = word_frame.winfo_reqwidth() * SCREEN_SCALE

            # Check if adding the next word would exceed the available width
            if self.cumulative_width + word_width + WORD_PAD > self.canvas_w:
                self.cumulative_width = (
                    WORD_PAD  # Reset cumulative width for the new row
                )
                self.cumulative_height += self.word_height + WORD_PAD

            word_frame.place(
                x=self.cumulative_width, y=self.cumulative_height, anchor="nw"
            )

            self.cumulative_width += word_width + WORD_PAD

    def scroll_lines(self):
        iterations = 10

        # Incremental movement in pixels per iteration
        movement_per_iteration = (self.word_height + WORD_PAD) / iterations

        # Define a recursive function for smooth animation
        def move_word_frame_smoothly(
            word_frame, current_x, current_y, target_y, iteration
        ):
            if iteration > 0:
                new_y = current_y - movement_per_iteration

                word_frame.place(x=current_x, y=new_y)

                # Schedule the next movement
                self.after(
                    10,
                    move_word_frame_smoothly,
                    word_frame,
                    current_x,
                    new_y,
                    target_y,
                    iteration - 1,
                )

        for word_frame in self.canvas.winfo_children():
            current_y = word_frame.winfo_y() * SCREEN_SCALE
            current_x = word_frame.winfo_x() * SCREEN_SCALE
            target_y = current_y - self.word_height - WORD_PAD

            # Start the smooth animation
            move_word_frame_smoothly(
                word_frame, current_x, current_y, target_y, iterations
            )
            self.canvas.update()

    def entry_text_callback(self, var=None, index=None, mode=None):
        word_frame = self.canvas.winfo_children()[self.active_word_index]
        word_entered = self.entry_text.get()

        if word_entered != "" and word_entered[-1] == " ":
            self.check_final_word()
            self.next_word()
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
        word_frame = self.canvas.winfo_children()[self.active_word_index]
        word_frame.configure(fg_color="transparent")
        self.active_word_index += 1
        self.entry_text.set("")
        next_word_frame = self.canvas.winfo_children()[self.active_word_index]
        self.set_active_word()

        if (next_word_frame.winfo_y() * SCREEN_SCALE) > (
            3 * WORD_PAD + 2 * self.word_height
        ):
            self.scroll_lines()
            for word_frame in self.canvas.winfo_children():
                if word_frame.winfo_y() * SCREEN_SCALE < 0:
                    word_frame.destroy()
                    self.active_word_index -= 1
                else:
                    break
            self.configure_event_handler()

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
        if is_correct:
            text_color = "blue"
        else:
            text_color = "red"
        for letter_frame in word_frame.winfo_children():
            letter_frame.configure(text_color=text_color)
        word_frame.configure(fg_color="transparent")
