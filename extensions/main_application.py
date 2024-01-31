# Standard library imports
import os

# Third-party library imports
from PIL import Image
from customtkinter import CTk, set_appearance_mode, CTkLabel, CTkFrame, CTkImage


# Local imports
from views import *
from utils import SUBTITLE_FONT, TITLE_FONT


class MainApplication(CTk):
    """
    MainApplication class represents the main application window.

    This class extends Tk and serves as the main application window. It contains methods for initializing
    the main view, handling the switching of views, and running the main application loop.

    Parameters:
        *args, **kwargs: Additional arguments passed to the Tk constructor.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the MainApplication.

        Parameters:
        *args, **kwargs: Additional arguments passed to the Tk constructor.
        """
        super().__init__(*args, **kwargs)
        self.MainView = MainView
        self.ResultView = ResultView

        # Initialize the appearance mode to "system"
        set_appearance_mode("system")

        self.current_view = None

        # Initialize Window
        self.title("Typing Speed Test")
        self.iconbitmap(os.path.join("resources", "images", "logo.ico"))

        # Calculate the window dimensions to 80% of the screen
        self.window_w = int(self.winfo_screenwidth() * 0.8)
        self.window_h = int(self.winfo_screenheight() * 0.8)

        # Calculate the position of the screen so it will be centered
        self.x = (self.winfo_screenwidth() // 2) - (self.window_w // 2)
        self.y = (self.winfo_screenheight() // 2) - (self.window_h // 2)

        # Set the window geometry
        self.geometry(f"{self.window_w}x{self.window_h}+{self.x}+{self.y}")

        # initialize Title
        self.initialize_titles()

        self.after(50, lambda: self.switch_view(self.MainView))

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
        self.subtitle_label = CTkLabel(
            self.titles_frame, text="Typing Speed Test", font=SUBTITLE_FONT
        )
        self.subtitle_label.pack()
        self.title_label = CTkLabel(
            self.titles_frame, text="Test your typing ability", font=TITLE_FONT
        )
        self.title_label.pack()

    def switch_view(self, view_class, *args, **kwargs):
        """Switches to a new view and destroys the current one.

        Args:
            view_class (class): The class of the view to switch to.
            *args: Additional positional arguments for the new view.
            **kwargs: Additional keyword arguments for the new view.
        """
        selected_view = view_class(self, self.switch_view, *args, **kwargs)

        if self.current_view:
            self.current_view.destroy()

        selected_view.pack(fill="both", expand=True)
        self.current_view = selected_view
