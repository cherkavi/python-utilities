from typing import List, Set
from unittest import TestCase
import filter_brackets


class TestMarkers(TestCase):
    def test_filter_lines_without_any_marker(self):
        # given
        data: List[str] = []
        with open("test-data-01.txt") as file:
            data = file.readlines()
        # when - no filtering, all text should be inside
        result: List[str] = filter_brackets.filter_lines(data, set())
        # then
        self.assertEqual(8, len(result), "full amount of strings")
        self.assertTrue(
            "just an example of 'how to use it'. Or, maybe, even more." in result
        )

    def test_filter_lines_with_not_existing_markers(self):
        # given
        data: List[str] = []
        with open("test-data-01.txt") as file:
            data = file.readlines()
        # when
        result: List[str] = filter_brackets.filter_lines(data, {"[xy]", "[yz]"})
        # then
        self.assertEqual(len(result), 4, "amount of string without any markers")
        self.assertTrue("that markers." in result)
        self.assertTrue(" still doesn't have them." in result)
        self.assertTrue("at the end of the file" in result)

    def test_filter_lines_with_existing_markers(self):
        # given
        data: List[str] = []
        with open("test-data-01.txt") as file:
            data = file.readlines()
        # when
        result: List[str] = filter_brackets.filter_lines(
            data,
            {
                "[ab]",
            },
        )
        # then
        self.assertEqual(7, len(result), "amount of string without any markers")
        self.assertTrue(
            "just an example of 'how to use it'. Or, maybe, even more." in result,
            "ab included",
        )
        self.assertTrue(
            "this is. but not for all lines." in result, "bc marker is filtered out"
        )
        self.assertTrue(
            "are present. still doesn't have them." in result,
            "bc marker is filtered out",
        )
        self.assertTrue("two markers in the row." in result, "conjunction with bc")
        self.assertTrue("and this text." not in result, "filtered out")

    def test_filter_lines_with_existing_multi_marker(self):
        # given
        data: List[str] = []
        with open("test-data-01.txt") as file:
            data = file.readlines()
        # when
        result: List[str] = filter_brackets.filter_lines(data, {"[ab]", "[bc]"})
        # then
        self.assertEqual(8, len(result), "amount of string without any markers")
        self.assertTrue(
            "just an example of 'how to use it'. Or, maybe, even more." in result
        )
        self.assertTrue("that markers." in result, "show line without any marker")
        self.assertTrue("and this text." in result, "bc marker is filtered out")
        self.assertTrue(
            "and here I just forget to add dot " in result, "marker at the end"
        )
        self.assertTrue("two markers in the row." in result, "ab is present also")

    def test_filter_lines_with_multi_markers_inside(self):
        # given
        data: List[str] = []
        with open("test-data-02.txt") as file:
            data = file.readlines()
        # when
        result: List[str] = filter_brackets.filter_lines(data, {"[bc]"})
        # then
        self.assertEqual(6, len(result), "amount of string without any markers")
        self.assertTrue(
            " internal data in the file." in result, "marker inside the line"
        )
        self.assertTrue(
            " internal data from file. " in result,
            "marker inside the line with mandatory []",
        )
        self.assertTrue("that should be considered." in result, "no markers")
        self.assertTrue(
            "as necessary. But not a mandatory" in result,
            "multi markers inside the line",
        )
        self.assertTrue(
            "filtered: with precedence              " in result,
            "[] has precedence over other",
        )

    def test_filter_lines_with_prefix_with_empty_markers(self):
        # given
        data: List[str] = []
        with open("test-data-04.txt") as file:
            data = file.readlines()
        # when
        result: List[str] = filter_brackets.filter_lines(data, {"[xy]"})
        # then
        self.assertEqual(2, len(result), "amount of string without any markers")
        self.assertTrue(
            "- my third data:  option four" in result, "last chunk without any marker"
        )
        self.assertTrue(
            "- my fourth data:  just a text " in result, "last chunk with []"
        )

    def test_filter_lines_with_prefix_with_markers(self):
        # given
        data: List[str] = []
        with open("test-data-04.txt") as file:
            data = file.readlines()
        # when
        result: List[str] = filter_brackets.filter_lines(data, {"[ab]"})
        # then
        self.assertEqual(4, len(result), "amount of string without any markers")
        self.assertTrue(
            '- my first data:  option one' in result,
            "with prefix, without last comma",
        )
        self.assertTrue(
            '- my second data:  just an information' in result,
            "with prefix, with filtered data",
        )
        self.assertTrue(
            '- my third data:  option three, option four' in result,
            "with prefix, with filtered data, with chunk without any marker at the end",
        )
        self.assertTrue(
            '- my fourth data:  just a text ' in result,
            "with prefix, with filtered data, with chunk with always-marker at the end",
        )


    def test_filter_lines_with_control_marker(self):
        # given
        data: List[str] = []
        with open("test-data-05.txt") as file:
            data = file.readlines()
        # when
        result: List[str] = filter_brackets.filter_lines(data, {"[ab]", "[control_two]"})
        self.assertEqual(2, len(result), "amount of string without any markers")
        self.assertTrue('  remove last version two' in result, "control marker")
        self.assertTrue('not a last, in the line ' in result, "without control marker")

class GetMarkersTest(TestCase):
    def test_get_markers(self):
        # given
        line = "are present.[ab] some lines[bcde] still doesn't have[fgh10] them.[last_comma]"
        # when
        markers = filter_brackets.get_markers(line)
        # then
        self.assertEqual(4, len(markers), "amount of markers")
        self.assertTrue("[ab]" in markers)
        self.assertTrue("[bcde]" in markers)
        self.assertTrue("[fgh10]" in markers)
        self.assertTrue("[last_comma]" in markers)


class TextChunkTest(TestCase):
    def test_get_text_without_markers(self):
        # given
        control_text: str = "this is simple text"
        chunk: filter_brackets.TextChunk = filter_brackets.TextChunk(control_text)
        # when, then
        self.assertEqual(control_text, chunk.get_text(None))
        self.assertTrue(control_text, chunk.get_text({}))
        self.assertTrue(control_text, chunk.get_text(set()))

    def test_chunk_filtering(self):
        # given
        control_text: str = "this is simple text"
        chunk: filter_brackets.TextChunk = filter_brackets.TextChunk(control_text)
        # when
        chunk.add_marker("[ab]")
        chunk.add_marker("[bc]")
        # then
        self.assertEqual(control_text, chunk.get_text({"[ab]"}))
        self.assertEqual(control_text, chunk.get_text({"[bc]"}))
        self.assertEqual(control_text, chunk.get_text({"[bc]", "[ab]"}))
        self.assertEqual(None, chunk.get_text({"[wa]", "[xy]"}))

    def test_get_nearest_marker(self):
        # given
        line: str = "[bc]this is[ab] line for[bc] analyzing[ab]"
        markers: Set[str] = filter_brackets.get_markers(line)
        # when
        nearest_marker: str = filter_brackets.get_nearest_marker(line, markers)
        # then
        self.assertEqual("[bc]", nearest_marker, "nearest marker in line - 0 position")

        # given
        line: str = "this is[ab] line for[bc] analyzing[ab]"
        markers: Set[str] = filter_brackets.get_markers(line)
        # when
        nearest_marker: str = filter_brackets.get_nearest_marker(line, markers)
        # then
        self.assertEqual("[ab]", nearest_marker, "nearest marker in line")

        # given
        line: str = "this is line without markers"
        markers: Set[str] = filter_brackets.get_markers(line)
        # when
        nearest_marker: str = filter_brackets.get_nearest_marker(line, markers)
        # then
        self.assertEqual(None, nearest_marker, "no markers in line")

        # given
        line: str = "this is line with empty marker[]"
        markers: Set[str] = filter_brackets.get_markers(line)
        # when
        nearest_marker: str = filter_brackets.get_nearest_marker(line, markers)
        # then
        self.assertEqual("[]", nearest_marker, "empty marker in line ")

    def test_get_chunks_from_line(self):
        # given
        line: str = "[bc]this is[ab][bc][db] line for[bc] analyzing[ab] [bd] always text[] also there"
        markers: Set[str] = filter_brackets.get_markers(line)
        # when
        chunks: List[filter_brackets.TextChunk] = filter_brackets.get_chunks_from_line(
            line, markers
        )
        # then
        self.assertEqual(7, len(chunks), "5 chunks in line")
        self.assertEqual({"[bc]"}, chunks[0].markers, "chunk-0 markers")
        self.assertEqual("", chunks[0].text, "chunk-0 text")
        self.assertEqual({"[ab]", "[bc]", "[db]"}, chunks[1].markers, "chunk-1 markers")
        self.assertEqual("this is", chunks[1].text, "chunk-1 text")
        self.assertEqual({"[bc]"}, chunks[2].markers, "chunk-2 markers")
        self.assertEqual(" line for", chunks[2].text, "chunk-2 text")
        self.assertEqual({"[ab]"}, chunks[3].markers, "chunk-3 markers")
        self.assertEqual(" analyzing", chunks[3].text, "chunk-3 text")
        self.assertEqual({"[bd]"}, chunks[4].markers, "chunk-4 markers")
        self.assertEqual(" ", chunks[4].text, "chunk-4 text")
        self.assertEqual(set(), chunks[5].markers, "chunk-5 markers")
        self.assertEqual(" always text", chunks[5].text, "chunk-5 text")
        self.assertEqual(set(), chunks[6].markers, "chunk-6 markers")
        self.assertEqual(" also there", chunks[6].text, "chunk-6 text")

    def test_remove_last_comma(self):
        # given
        data: List[str] = []
        with open("test-data-03.txt") as file:
            data = file.readlines()
        # when
        result: List[str] = filter_brackets.filter_lines(data, {"[ab]", "[bc]"})
        # then
        self.assertEqual(len(result), 3, "amount of string without any markers")
        self.assertTrue("remove last, comma, " not in result)
        self.assertTrue("remove last, comma " not in result)
        self.assertTrue("  remove last, comma" in result)
        self.assertTrue("not a last, comma, in the line " in result)
