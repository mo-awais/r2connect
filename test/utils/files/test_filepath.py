import unittest

from utils.files.filepath import Filepath


class TestFilepath(unittest.TestCase):
    filepath = Filepath()

    def test_safe_filepath(self):
        self.assertEqual("F-A-Costs.html", self.filepath.safe_filepath("F&A Costs.html"))
        self.assertEqual("F-A--Costs.html", self.filepath.safe_filepath("F%A&/Costs.html"))
        self.assertEqual("F-A-Costs.html", self.filepath.safe_filepath("F{A}Costs.html"))
        self.assertEqual("F-Costs.html", self.filepath.safe_filepath("F?Costs.html"))
        self.assertEqual("F-Costs.html", self.filepath.safe_filepath("'F-Costs.html'"))
