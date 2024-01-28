# Standard library imports
import ctypes

# Third-party library imports


# Local imports


TITLE_FONT = ("Ubuntu", 60, "bold")
SUBTITLE_FONT = ("Georgia", 30, "bold")
TEXT_FONT = ("Ubuntu", 40)

WORD_PAD = 20
SCREEN_SCALE = 1 / (ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100)
