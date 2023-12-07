import unittest
import Foogle


class Test(unittest.TestCase):
    def test_one_word(self):
        self.assertEqual(
            (
                Foogle.Finder(["file1.txt", "file2.txt", "file3.txt"]).phrase_query(
                    "видит"
                )
            ),
            ["file1.txt"],
        )

    def test_phrase(self):
        self.assertEqual(
            (Foogle.Finder(["file1.txt"]).phrase_query("королевна видит")), ["file1.txt"]
        )

    def test_many_files(self):
        self.assertEqual(
            (Foogle.Finder(["file1.txt", "file2.txt", "file3.txt"]).phrase_query("да")),
            ["file1.txt", "file2.txt"],
        )

    def test_rank_results(self):
        self.assertEqual(
            (
                Foogle.Finder(["file1.txt", "file2.txt", "file3.txt"]).phrase_query(
                    "ёмаё"
                )
            )[0],
            "file2.txt",
        )


if __name__ == "__main__":
    unittest.main()
