import unittest
import Foogle


class Test(unittest.TestCase):
    def test_find(self):
        self.assertEqual(
            (Foogle.Finder("tests").find("бежала на трех ногах|царевна|королевна", ".txt")).pop(),
            "file1.txt")

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
            'Не найдено',
        )

    def test_not(self):
        self.assertEqual(
            (Foogle.Finder("tests").find("королевна|лягушка|-ёмаё", ".txt")),
            'Не найдено',
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


if __name__ == "__main__":
    unittest.main()
