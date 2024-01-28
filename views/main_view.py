# Standard library imports
import os

# Third-party library imports
from customtkinter import CTkFrame, CTkLabel, CTkImage
from PIL import Image


# Local imports
from utils import SUBTITLE_FONT, TITLE_FONT, TEXT_FONT, SCREEN_SCALE, WORD_PAD


class MainView(CTkFrame):
    def __init__(self, parent, switch_view, *args, **kwargs):
        CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.switch_view = switch_view

        self.words_set = {
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
        }

        self.word_height = None
        self.cumulative_width = WORD_PAD
        self.cumulative_height = WORD_PAD

        # initialize Title
        self.initialize_titles()

        # Initialize Canvas
        self.initialize_canvas()

        self.bind("<Configure>", self.initialize_word_layout)

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
        self.create_word_frame("abc")
        self.canvas_h = self.word_height * 3 + WORD_PAD * 4
        self.canvas.configure(height=self.canvas_h)

    def create_word_frame(self, word):
        word_label = CTkFrame(self.canvas)
        for letter in word:
            letter_label = CTkLabel(word_label, text=letter, font=TEXT_FONT)
            letter_label.pack(side="left")
        self.canvas.update_idletasks()
        if not self.word_height:
            self.word_height = word_label.winfo_reqheight() * SCREEN_SCALE

    def initialize_word_layout(self, event=None):
        while self.cumulative_height < 3 * self.word_height + 4 * WORD_PAD:
            self.create_word_frame("abc")
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
