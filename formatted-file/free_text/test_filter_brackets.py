from typing import List
from unittest import TestCase

import filter_brackets


class TestMarkers(TestCase):
    def test_filter_lines_without_any_marker(self):
        # given
        data: List[str] = []
        with open("test-data-01.txt") as file:
            data = file.readlines()
        # when
        result: List[str] = filter_brackets.filter_lines(data, set())
        # then
        self.assertEqual(3, len(result), "amount of string without any markers")
        self.assertTrue("that markers." in result)
        self.assertTrue("just an example of 'how to use it'." in result)
        self.assertTrue("at the end of the file" in result)

    def test_filter_lines_with_not_existing_markers(self):
        # given
        data: List[str] = []
        with open("test-data-01.txt") as file:
            data = file.readlines()
        # when
        result: List[str] = filter_brackets.filter_lines(data, {"xy", "yz"})
        # then
        self.assertEqual(len(result), 3, "amount of string without any markers")

    def test_filter_lines_with_existing_markers(self):
        # given
        data: List[str] = []
        with open("test-data-01.txt") as file:
            data = file.readlines()
        # when
        result: List[str] = filter_brackets.filter_lines(data, {"ab", })
        # then
        self.assertEqual(7, len(result), "amount of string without any markers")
        self.assertFalse("and this text." in result, "bc marker is filtered out")
        self.assertTrue("and here I just forget to add dot ." in result, "single line without dot with ab marker")
        self.assertFalse("are present. some lines still doesn't have them." in result, "marker inside the line")

    def test_filter_lines_with_existing_marker_inside_line(self):
        # given
        data: List[str] = []
        with open("test-data-01.txt") as file:
            data = file.readlines()
        # when
        result: List[str] = filter_brackets.filter_lines(data, {"ab", })
        # then
        self.assertEqual(7, len(result), "amount of string without any markers")
        self.assertFalse("and this text." in result, "bc marker is filtered out")
        self.assertTrue("and here I just forget to add dot ." in result, "single line without dot with ab marker")
        self.assertTrue("two markers in the row." in result, "ab is present also")

    def test_filter_lines_with_existing_multi_marker(self):
        # given
        data: List[str] = []
        with open("test-data-01.txt") as file:
            data = file.readlines()
        # when
        result: List[str] = filter_brackets.filter_lines(data, {"ab", "bc"})
        # then
        self.assertEqual(8, len(result), "amount of string without any markers")
        self.assertTrue("that markers." in result, "show line without any marker")
        self.assertTrue("and this text." in result, "bc marker is filtered out")
        self.assertTrue("and here I just forget to add dot ." in result, "single line without dot with ab marker")
        self.assertTrue("two markers in the row." in result, "ab is present also")

    def test_filter_lines_without_markers(self):
        # given
        data: List[str] = []
        with open("test-data-02.txt") as file:
            data = file.readlines()
        # when
        result: List[str] = filter_brackets.filter_lines(data, {})
        # then
        self.assertEqual(2, len(result), "amount of string without any markers")
        self.assertTrue("that should be considered." in result, "no markers")
        self.assertTrue("in the file." in result, "no markers")


    def test_filter_lines_with_markers_inside(self):
        # given
        data: List[str] = []
        with open("test-data-02.txt") as file:
            data = file.readlines()
        # when
        result: List[str] = filter_brackets.filter_lines(data, {"bc"})
        # then
        self.assertTrue(3, len(result), "amount of string without any markers")
        self.assertTrue(" internal data in the file." in result, "marker inside the line")
        self.assertTrue("as necessary. But not a mandatory." in result, "multi markers inside the line")


class TestRemoveBrackets(TestCase):
    def test_remove_markers(self):
        # given
        line: str = "this is [ab]. new file with markers[bc]. but not for all lines[ab]."
        # when
        result: str = filter_brackets.remove_markers(line, {"ab", "bc"})
        print(result)
        # then
        self.assertTrue("[ab]" not in result)
        self.assertTrue("[bc]" not in result)

    def test_remove_marker(self):
        # given
        line: str = "this is [ab]. new file with markers[bc]. but not for all lines[ab]."
        # when
        result: str = filter_brackets.remove_markers(line, {"ab", })
        print(result)
        # then
        self.assertTrue("[ab]" not in result)
        self.assertTrue("[bc]" in result)
