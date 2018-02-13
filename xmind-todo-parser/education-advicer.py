#!/usr/bin/env python
"""
parse XMind document and retrieve
all elements with notes (time:, tag: )
and with markers: "red flag", "exercise".
skip.txt contains lines to skip from output
"""

import xmind
# git clone https://github.com/xmindltd/xmind-sdk-python.git,   python setup.py install
import sys


DELIMITERS = [":", "="]


def parse_notes(notes, param):
    for each_line in str(notes).splitlines():
        line = each_line.strip().lower()
        if not(line.startswith(param)):
            continue
        for delimiter in DELIMITERS:
            delimiter_index = line.index(delimiter, len(param))
            if delimiter_index >= 0:
                return line[delimiter_index+1:].strip()
    return None


class Leaf:

    def __init__(self, topic):
        self.name = topic.getTitle().encode("utf-8").strip()
        if topic.getNotes():
            notes = topic.getNotes().getContent().encode("utf-8").strip()
            self.time = parse_notes(notes, "time")
            if self.time:
                self.time = int(self.time)
            self.tag = parse_notes(notes, "tag")
            if self.tag:
                self.tag = [each_tag.strip() for each_tag in self.tag.split(",")]
            else:
                self.tag = []
        else:
            self.time = None
            self.tag = None
        if topic.getHyperlink():
            self.url = topic.getHyperlink().encode("utf-8").strip()
        else:
            self.url = None
        if topic.getMarkers() and len(topic.getMarkers()) > 0:
            self.markers = [each_marker.getMarkerId().name.encode("utf-8") for each_marker in topic.getMarkers()]
        else:
            self.markers = []

    def __str__(self):
        return str(self.name) + " >>> " + str(self.time) + ", " + str(self.tag) + ", " + str(self.markers) + ", " \
               + str(self.url)

    def to_html(self):
        return '<a href="%s">%s</a> <sup>%s</sup>' % (self.url if self.url else "", self.name, self.time if self.time else "")

    @staticmethod
    def is_topic_searchable(root):
        return root.getNotes() or root.getMarkers()


def walk_through_children(root, topics):
    if Leaf.is_topic_searchable(root):
        topics.add(Leaf(root))
    subtopics = root.getSubTopics()
    if subtopics and len(subtopics) > 0:
        for subtopic in subtopics:
            walk_through_children(subtopic, topics)


def print_html_block(block_name, elements):
    print("<section> <h3> %s </h3> <ul>" % (block_name,))
    for each in elements:
        print("<li>%s</li>" % (each.to_html()))
    print("</ul></section><br />")


def read_from_file(file_name):
    return_value = set()
    try:
        with open(file_name, "r") as f:
            for each_line in f:
                return_value.add(each_line.strip())
    except:
        pass
    return return_value


def main(parameters):
    path = parameters[0]
    time = int(parameters[1]) if len(parameters) >= 2 else None
    workbook = xmind.load(path)
    topics = set()
    walk_through_children(workbook.getPrimarySheet().getRootTopic(), topics)

    skip = read_from_file("skip.txt")

    red_flags = set([topic for topic in topics if "flag-red" in topic.markers and topic.name not in skip])
    print_html_block("RED FLAG", red_flags-skip)

    exercises = set([topic for topic in topics if "c_symbol_exercise" in topic.markers and topic.name not in skip])
    print_html_block("EXERCISES", exercises-skip)

    if time:
        print_html_block("by time: " + str(time),
                         [topic for topic in (topics-red_flags-exercises-skip)
                          if topic.time and topic.time <= time and topic.name not in skip])


if len(sys.argv) < 2:
    print("name of the file should be specified")
else:
    main(sys.argv[1:])
