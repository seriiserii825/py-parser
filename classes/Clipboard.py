import pyperclip


class Clipboard:
    @staticmethod
    def copy(text):
        pyperclip.copy(text)

    @staticmethod
    def paste():
        return pyperclip.paste()
