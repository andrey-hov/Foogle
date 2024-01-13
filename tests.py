import unittest
import Foogle
import Index
import os


class Test(unittest.TestCase):
    def test_find(self):
        self.assertEqual(
            (
                Foogle.Finder("tests").find(
                    "бежала на трех ногах|царевна|королевна", ".txt"
                )
            ).pop(),
            "file1.txt",
        )

    def test_one_word(self):
        self.assertEqual(
            (Foogle.Finder("tests").phrase_query("видит", ".txt")), ["file1.txt"]
        )

    def test_or(self):
        self.assertEqual(
            sorted(list((Foogle.Finder("tests").find("ёмаё|лягушка", ".txt")))),
            ["file1.txt", "file2.txt"],
        )

    def test_and(self):
        self.assertEqual(
            sorted(list((Foogle.Finder("tests").find("добру молодцу", ".txt")))),
            ["file2.txt"],
        )

    def test_not_and(self):
        self.assertEqual(
            (Foogle.Finder("tests").find("королевна|-да ёмаё", ".txt")),
            "Не найдено",
        )

    def test_not(self):
        self.assertEqual(
            (Foogle.Finder("tests").find("королевна|лягушка|-ёмаё", ".txt")),
            "Не найдено",
        )

    def test_many_files(self):
        self.assertEqual(
            (Foogle.Finder("tests").phrase_query("да", ".txt")),
            ["file1.txt", "file2.txt"],
        )

    def test_rank_results(self):
        self.assertEqual(
            (Foogle.Finder("tests").phrase_query("ёмаё", ".txt"))[0], "file2.txt"
        )

    def test_lang(self):
        self.assertEqual(
            (Foogle.Finder("tests").phrase_query("want", ".txt")),
            ["file3.txt"],
        )

    def test_format_rtf(self):
        self.assertEqual(
            (Foogle.Finder("tests").phrase_query("want", ".rtf")),
            ["Не найдено"],
        )

    def test_format_jpg(self):
        self.assertEqual(
            (Foogle.Finder("tests").phrase_query("want", ".jpg")),
            ["Не найдено"],
        )

    def test_index_file(self):
        self.assertDictEqual(
            (Index.BuildIndex.index_file(["hello", "my", "friend", "hello"])),
            {"hello": [0, 3], "my": [1], "friend": [2]},
        )

    def test_process_file(self):
        os.chdir("tests")
        self.assertDictEqual(
            (Index.BuildIndex(["file.txt"]).file_to_terms),
            {"file.txt": ["hello", "my", "friend", "hello"]},
        )
        os.chdir(r"../")

    def test_make_indices(self):
        os.chdir("tests")
        self.assertDictEqual(
            (
                Index.BuildIndex(["file.txt"]).make_indices(
                    Index.BuildIndex(["file.txt"]).file_to_terms
                )
            ),
            {"file.txt": {"hello": [0, 3], "my": [1], "friend": [2]}},
        )
        os.chdir(r"../")

    def test_full_index(self):
        os.chdir("tests")
        self.assertDictEqual(
            (Index.BuildIndex(["file.txt"]).fullIndex()),
            {
                "hello": {"file.txt": [0, 3]},
                "my": {"file.txt": [1]},
                "friend": {"file.txt": [2]},
            },
        )
        os.chdir(r"../")

    def test_document_frequency(self):
        os.chdir("tests")
        self.assertEqual(
            (Index.BuildIndex(["file.txt"]).document_frequency("hello")), 1
        )
        os.chdir(r"../")


if __name__ == "__main__":
    unittest.main()
