from pathlib import Path
import sys


class PathHelper:
    def __init__(self):
        # Path to the current script (where this class is defined)
        self.script_path = Path(__file__).resolve()
        self.script_dir = self.script_path.parent

        # Path to the entry point (the script passed to python)
        self.entry_point = Path(sys.argv[0]).resolve()
        self.entry_dir = self.entry_point.parent

        # Current working directory (where python was called from)
        self.cwd = Path.cwd()

    @property
    def script(self) -> Path:
        return self.script_path

    @property
    def script_directory(self) -> Path:
        return self.script_dir
