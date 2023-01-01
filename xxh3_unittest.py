import unittest
import xxh3
from io import StringIO
from os import getcwd
from unittest.mock import patch


class Arguments:

    def __init__(
        self,
        TARGET_PATH: str,
        check_file: str = "",
        duplicates: bool | None = None,
        recursive: bool | None = None,
    ):
        self.TARGET_PATH = TARGET_PATH
        self.check_file = check_file
        self.duplicates = duplicates
        self.recursive = recursive


class Tests(unittest.TestCase):

    working_directory: str = getcwd()

    def test_path_does_not_exist(self):
        args = Arguments("absent_file")
        with self.assertRaises(SystemExit):
            xxh3.main(args)

    def test_hexdigest_function(self):
        self.assertEqual(
            xxh3.xxh3('./fixtures/directory1/file1'), "8bb820c8bfd319e9"
        )

    def test_file(self):
        args = Arguments(
            "./fixtures/directory1/file1"
        )
        with patch('sys.stdout', new=StringIO()) as xxh3_out:
            result = (
                f"8bb820c8bfd319e9 '{self.working_directory}"
                "/fixtures/directory1/file1'\n"
            )
            xxh3.main(args)
            self.assertEqual(xxh3_out.getvalue(), result)

    def test_directory(self):
        self.maxDiff = None
        args = Arguments(
            "./fixtures/directory1/"
        )
        with patch('sys.stdout', new=StringIO()) as xxh3_out:
            result = (
                f"b934de79df15dc7a '{self.working_directory}"
                "/fixtures/directory1/file5'\n"

                f"b934de79df15dc7a '{self.working_directory}"
                "/fixtures/directory1/file4'\n"

                f"bd4bf76d31884603 '{self.working_directory}"
                "/fixtures/directory1/file6'\n"

                f"8bb820c8bfd319e9 '{self.working_directory}"
                "/fixtures/directory1/file1'\n"

                f"e26ddd6506044599 '{self.working_directory}"
                "/fixtures/directory1/file3'\n"

                f"e26ddd6506044599 '{self.working_directory}"
                "/fixtures/directory1/file2'\n"
            )
            xxh3.main(args)
            self.assertEqual(xxh3_out.getvalue(), result)

    def test_directory_recursively(self):
        self.maxDiff = None
        args = Arguments(
            "./fixtures/directory1/",
            recursive=True
        )
        with patch('sys.stdout', new=StringIO()) as xxh3_out:
            result = (
                f"b934de79df15dc7a '{self.working_directory}"
                "/fixtures/directory1/file5'\n"

                f"b934de79df15dc7a '{self.working_directory}"
                "/fixtures/directory1/file4'\n"

                f"bd4bf76d31884603 '{self.working_directory}"
                "/fixtures/directory1/file6'\n"

                f"8bb820c8bfd319e9 '{self.working_directory}"
                "/fixtures/directory1/file1'\n"

                f"e26ddd6506044599 '{self.working_directory}"
                "/fixtures/directory1/file3'\n"

                f"e26ddd6506044599 '{self.working_directory}"
                "/fixtures/directory1/file2'\n"

                f"f9ee32e48a61e285 '{self.working_directory}"
                "/fixtures/directory1/subdir1/z'\n"

                f"7eee3d4a309e8304 '{self.working_directory}"
                "/fixtures/directory1/subdir1/x'\n"
            )

    def test_directory_duplicates(self):
        self.maxDiff = None
        args = Arguments(
            "./fixtures/directory1/",
            duplicates=True
        )
        with patch('sys.stdout', new=StringIO()) as xxh3_out:
            result = (
                f"b934de79df15dc7a '{self.working_directory}"
                "/fixtures/directory1/file5'\n"

                f"b934de79df15dc7a '{self.working_directory}"
                "/fixtures/directory1/file4'\n"

                f"bd4bf76d31884603 '{self.working_directory}"
                "/fixtures/directory1/file6'\n"

                f"8bb820c8bfd319e9 '{self.working_directory}"
                "/fixtures/directory1/file1'\n"

                f"e26ddd6506044599 '{self.working_directory}"
                "/fixtures/directory1/file3'\n"

                f"e26ddd6506044599 '{self.working_directory}"
                "/fixtures/directory1/file2'\n"

                f"=b934de79df15dc7a '{self.working_directory}"
                "/fixtures/directory1/file4'\n"

                f"=e26ddd6506044599 '{self.working_directory}"
                "/fixtures/directory1/file2'\n"
            )

    def test_directory_duplicates_recursively(self):
        self.maxDiff = None
        args = Arguments(
            "./fixtures/directory1/",
            duplicates=True,
            recursive=True
        )
        with patch('sys.stdout', new=StringIO()) as xxh3_out:
            result = (
                f"b934de79df15dc7a '{self.working_directory}"
                "/fixtures/directory1/file5'\n"

                f"b934de79df15dc7a '{self.working_directory}"
                "/fixtures/directory1/file4'\n"

                f"bd4bf76d31884603 '{self.working_directory}"
                "/fixtures/directory1/file6'\n"

                f"8bb820c8bfd319e9 '{self.working_directory}"
                "/fixtures/directory1/file1'\n"

                f"e26ddd6506044599 '{self.working_directory}"
                "/fixtures/directory1/file3'\n"

                f"e26ddd6506044599 '{self.working_directory}"
                "/fixtures/directory1/file2'\n"

                f"f9ee32e48a61e285 '{self.working_directory}"
                "/fixtures/directory1/subdir1/z'\n"

                f"7eee3d4a309e8304 '{self.working_directory}"
                "/fixtures/directory1/subdir1/x'\n"

                f"=b934de79df15dc7a '{self.working_directory}"
                "/fixtures/directory1/file4'\n"

                f"=e26ddd6506044599 '{self.working_directory}"
                "/fixtures/directory1/file2'\n"
            )
            xxh3.main(args)
            self.assertEqual(xxh3_out.getvalue(), result)


if __name__ == '__main__':
    unittest.main()
