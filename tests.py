import unittest
import Foogle
import os


class Test(unittest.TestCase):
    def test_find(self):
        self.assertEqual(
            (Foogle.Finder("tests").find("бежала на трех ногах|царевна|королевна", ".txt")).pop(),
            "file1.txt"
        )

    def test_one_word(self):
        self.assertEqual(
            (Foogle.Finder("tests").phrase_query("видит", ".txt")),
            ["file1.txt"]
        )

    def test_phrase(self):
        self.assertEqual(
            (Foogle.Finder("file1.txt").phrase_query("королевна видит", ".txt")),
            ["file1.txt"]
        )

    def test_free_text(self):
        self.assertEqual(
            (Foogle.Finder("file1.txt").free_text_query("королевна видит")),
            ["file1.txt"]
        )

    def test_many_files(self):
        self.assertEqual(
            (Foogle.Finder("tests").phrase_query("да", ".txt")),
            ["file1.txt", "file2.txt"]
        )

    def test_rank_results(self):
        self.assertEqual(
            (Foogle.Finder("tests").phrase_query("ёмаё", ".txt"))[0],
            "file2.txt"
        )


if __name__ == "__main__":
    unittest.main()
