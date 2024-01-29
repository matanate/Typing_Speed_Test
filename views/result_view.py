# Standard library imports


# Third-party library imports
from customtkinter import CTkFrame

# Local imports


class ResultView(CTkFrame):
    def __init__(self, parent, switch_view, result=None, *args, **kwargs):
        CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.switch_view = switch_view
