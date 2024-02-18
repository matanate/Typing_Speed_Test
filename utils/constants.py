# Standard library imports
import sys

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


def get_screen_scale_factor():
    if sys.platform == "win32":
        import ctypes

        try:
            return 1 / (ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100)
        except Exception as e:
            print(f"Error retrieving scale factor on Windows: {e}")
            return 1.0  # default to 1.0 if there is an error

    elif sys.platform == "darwin":
        try:
            from AppKit import NSScreen

            return NSScreen.mainScreen().backingScaleFactor()
        except Exception as e:
            print(f"Error retrieving scale factor on macOS: {e}")
            return 1.0  # default to 1.0 if there is an error

    elif sys.platform.startswith("linux"):
        try:
            with open("/var/log/Xorg.0.log", "r") as f:
                for line in f:
                    if "dpi" in line:
                        dpi = int(line.split()[-1])
                        return 1 / (dpi / 100.0)
                return 1.0  # default to 1.0 if 'dpi' is not found in Xorg.0.log
        except Exception as e:
            print(f"Error retrieving scale factor on Linux: {e}")
            return 1.0  # default to 1.0 if there is an error

    else:
        print("Unsupported platform. Defaulting to scale factor of 1.0.")
        return 1.0  # default scale factor for unsupported platforms


# Get the scale factor
SCREEN_SCALE = get_screen_scale_factor()
