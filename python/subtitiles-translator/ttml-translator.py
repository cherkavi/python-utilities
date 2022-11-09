#!/usr/bin/env python3
# ./ttml-translator.py /path/to/times/text/markup/language
# <tt:body region="AmazonDefaultRegion">
#        <tt:div>
#            <tt:p begin="00:01:23.334" end="00:01:25.044">- Ja?<tt:br/>- Du wurdest enttarnt.</tt:p>
#            <tt:p begin="00:01:25.127" end="00:01:27.838">- Fahr sofort zur Botschaft.<tt:br/>- Okay.</tt:p>

import subprocess
import sys
from functools import reduce
from time import sleep
from typing import List
from xml.dom.minidom import parse, parseString, Element, Document, Node


def child_nodes_to_text(nodes):
    return reduce(lambda x, y: x + "\n" + y,
                  map(lambda _: _.nodeValue, filter(lambda _: _.nodeType == Node.TEXT_NODE, nodes)))


def translate_from_german(text):
    translation = subprocess.check_output(["trans", "--no-warn", "-source", "de", "-target", "ru", "-brief", text])
    sleep(3)
    return translation.decode('utf-8').rstrip()


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("can't find path to TimedTextMarkupLanguage file as input argument ")
        sys.exit(1)
    path_to_file = sys.argv[1]
    dom: Document = parse(path_to_file)
    components: List[Element] = [each_element for each_element in dom.getElementsByTagName("tt:p")]
    for each_component in components:
        print("===", each_component.getAttribute("begin"), each_component.getAttribute("end"))
        text = child_nodes_to_text(each_component.childNodes)
        #print(text, "\n", translate_from_german(text))
        print(text)
