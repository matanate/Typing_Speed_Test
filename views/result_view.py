# Standard library imports


# Third-party library imports
from customtkinter import CTkFrame, CTkLabel, CTkButton

# Local imports
from utils import SCORE_FONT, WRONG_WORDS_FONT, WRONG_WORDS_TITLE_FONT


class ResultView(CTkFrame):
    def __init__(self, parent, switch_view, *args, **kwargs):
        CTkFrame.__init__(self, parent, *args[1:], **kwargs)
        self.parent = parent
        self.switch_view = switch_view
        self.result = args[0]
        self.configure(fg_color="transparent")

        # Calculate the results
        self.calculate_from_result()

        # Initialize Score
        self.initialize_score()

        # Initialize restart button
        self.initialize_restart_btn()

    def calculate_from_result(self):
        total_time = 1
        self.potential_wpm = int(len(self.result) / total_time)
        self.wrong_words = []

        word_count = 0
        character_count = 0
        potential_character_count = 0

        for word_result in self.result:
            if word_result["is_correct"]:
                character_count += len(word_result["word"])
                word_count += 1
            else:
                potential_character_count += len(word_result["word"])
                self.wrong_words.append(
                    (word_result["word_entered"], word_result["word"])
                )
        potential_character_count += character_count

        self.correct_words = word_count
        self.cpm_score = int(character_count / total_time)
        self.potential_cpm_score = int(potential_character_count / total_time)
        self.wpm_score = int(word_count / total_time)

    def initialize_score(self):
        self.score_frame = CTkFrame(self)
        self.score_frame.pack()

        self.score_label = CTkLabel(
            self.score_frame,
            fg_color="transparent",
            text=f"Your Score: {self.cpm_score} CPM, (that is {self.wpm_score} WPM)",
            font=SCORE_FONT,
        )
        self.score_label.pack(pady=20)

        if self.wrong_words:
            self.congrats_label = CTkLabel(
                self.score_frame,
                fg_color="transparent",
                text=f"In reality, you typed {self.potential_cpm_score} CPM, but you made {len(self.wrong_words)} mistakes (out of {len(self.result)} words),\nwhich were not counted in the corrected scores.",
                font=WRONG_WORDS_TITLE_FONT,
            )
            self.congrats_label.pack(pady=10)

            self.wrong_label = CTkLabel(
                self.score_frame,
                fg_color="transparent",
                text=f"Your mistakes were:",
                font=WRONG_WORDS_FONT + ("bold",),
            )
            self.wrong_label.pack()
            for wrong_word in self.wrong_words:
                label = CTkLabel(
                    self.score_frame,
                    fg_color="transparent",
                    text=f'Instead of "{wrong_word[1]}", you typed "{wrong_word[0]}".',
                    font=WRONG_WORDS_FONT,
                )
                label.pack()
        else:
            self.congrats_label = CTkLabel(
                self.score_frame,
                fg_color="transparent",
                text=f"Congratulation! you typed {self.correct_words} words correctly!",
                font=WRONG_WORDS_TITLE_FONT,
            )
            self.congrats_label.pack()

    def initialize_restart_btn(self):
        self.restart_btn = CTkButton(
            self,
            text="Restart",
            command=lambda: self.switch_view(self.parent.MainView),
        )
        self.restart_btn.pack()
