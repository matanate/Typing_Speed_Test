# Standard library imports
import ctypes

# Fonts
TITLE_FONT = ("Ubuntu", 60, "bold")
SUBTITLE_FONT = ("Georgia", 30, "bold")
TEXT_FONT = ("Ubuntu", 40)
TIMERS_FONT = ("Ubuntu", 20)
SCORE_FONT = ("Ubuntu", 30, "bold")
WRONG_WORDS_TITLE_FONT = ("Ubuntu", 20, "bold")
WRONG_WORDS_FONT = ("Ubuntu", 15)

# Pading and Scaling
WORD_PAD = 20
SCREEN_SCALE = 1 / (ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100)
