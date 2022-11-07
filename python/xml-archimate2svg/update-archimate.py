"""
[Archimate editor](https://www.archimatetool.com/) doesn't have ability to export image from internal Archi format to SVG and enrich it with documentation information.
It is super useful when all your links that you saved for some elements in "Documentation" field will be "copyied" to SVG as links
Input Arguments:
{path to original Archimate file} { path to exported SVG file } {path to output SVG, that will be enriched with links}

if you want to automate process of exporting from Archi to SVG ( not working in headless mode ) - pay your attention to 
https://github.com/cherkavi/docker-images/blob/master/automation4app/Archi-svg-export.md
"""
from xml.dom.minidom import parse, parseString, Element
import sys
from typing import Dict


class ArchiDoc:
    def __init__(self, url, title):
        self.url = url
        self.title = title

# example of typing, generic type example
ArchiDocList = Dict[str, ArchiDoc]


def is_archimate_component(element):
    return element.getAttribute("xsi:type").startswith("archimate:") and element.hasChildNodes()


def is_element_has_documentation(element):
    # filter element by classtype, java "instance of" with shortName
    return element.__class__.__name__ == "Element" and element.tagName == "documentation"


def get_first_http_link(lines):
    splitted_lines = map(lambda x: x.split("\n"), lines)
    flatted_lines = [each_element for each_line in splitted_lines for each_element in each_line]
    trim_lines = map(lambda x: x.strip(), flatted_lines)
    lines_with_links = list(filter(lambda x: x.startswith("http"), trim_lines))
    return lines_with_links[0] if len(lines_with_links) > 0 else None


def archi_elements(path_to_source_file) -> ArchiDocList:
    """ find all elements inside 'archimate' that contain a description 
    return dictionary: text -> url
    """
    dom = parse(path_to_source_file)  # parse an XML file by name
    components = [each_element for each_element in dom.getElementsByTagName("element")
                  if is_archimate_component(each_element)]
    components_description = map(lambda x: (#0
                                            x.getAttribute("name"),
                                            #1
                                            "showTooltip(event)",
                                            #2
                                            " | ".join("".join([each_child.firstChild.nodeValue
                                             for each_child in x.childNodes
                                             if is_element_has_documentation(each_child)]).split("\n"))
                                            ),
                                 components)
    non_empty_description = filter(lambda x: x[2] is not None and len(x[2])>0, components_description)
    return dict((name, ArchiDoc(url, doc)) for name, url, doc in non_empty_description)


def has_attr_clip_path(element: Element):
    return element.hasAttribute("clip-path")


def save_xml_to_file(root_node, output_file_path):
    """ save minidom to file """
    with open(output_file_path, "w") as file:
        root_node.writexml(file)


def wrap_node_with_anchor(dom, url: str, title: str, xml_elements):
    """ replace current element with anchor and put current element inside it """
    for each_node in xml_elements:
        parent = each_node.parentNode
        parent.removeChild(each_node)
        anchor = dom.createElement("a")
        if url:
            anchor.setAttribute("onclick", url)
        if title:
            anchor.setAttribute("data-doc", title)
            anchor.setAttribute("xlink:title", title)
        anchor.appendChild(each_node)
        parent.appendChild(anchor)


def update_svg_elements(source_file, archimate_description:ArchiDocList, destination_file):
    """find all elements inside SVG file  """
    dom = parse(source_file) 
    # list of elements: xml_node, text, @clip-path
    svg_elements = [(each_element, each_element.firstChild.nodeValue, each_element.getAttribute("clip-path"))
                    for each_element in dom.getElementsByTagName("text")
                    if each_element.hasChildNodes() and has_attr_clip_path(each_element)]

    # generate dict: @clip_path -> [(text, xml_node) (text, xml_node)]
    groupped_by_clip = dict()
    for xml_element, text, clip_path in svg_elements:        
        if clip_path in groupped_by_clip:
            groupped_by_clip[clip_path].append((text, xml_element))
        else:
            groupped_by_clip[clip_path] = [(text, xml_element)]

    # generate dictionary: title -> xml nodes
    name_xmlnodes = dict()
    for _, value in groupped_by_clip.items():
        text = " ".join([each_element[0] for each_element in value])
        xml_elements = [each_element[1] for each_element in value]
        if text in name_xmlnodes:
            name_xmlnodes[text].extend(xml_elements)
        else:
            name_xmlnodes[text] = xml_elements

    # walk through all objects and wrap with <a>
    for (name, archiDoc) in archimate_description.items():
        if name in name_xmlnodes:
            wrap_node_with_anchor(dom, archiDoc.url, archiDoc.title, name_xmlnodes[name])

    save_xml_to_file(dom, destination_file)


def content_of_file(path_to_file: str)->str:
    with open(path_to_file, "r") as file:
        return "".join(file.readlines())


def add_javascript(svg_original:str, svg_updated: str, js_script:str):
    # open file
    dom = parse(svg_original)         
    # insert JavaScript 
    svg_root = dom.getElementsByTagName("svg")[0]
    script_element = dom.createElement("script")        
    script_element.setAttribute("type", "text/ecmascript")        
    ### not working with: 
    ### script_element.innerHTML = content_of_file(js_script)    
    ### script_element.text = content_of_file(js_script)    
    script_element.appendChild(dom.createCDATASection(content_of_file(js_script)))
    svg_root.appendChild(script_element)

    # tooltip placeholder
    svg_graphics = dom.getElementsByTagName("g")[0]
    svg_rect = dom.createElement("rect")
    svg_rect.setAttribute("id", "tooltip")
    svg_rect.setAttribute("style", "fill:rgb(255,255,0);display: none")
    svg_rect.setAttribute("onclick", "hideTooltip()")
    svg_rect.appendChild(dom.createElement("title"))

    svg_graphics.appendChild(svg_rect)

    # save file
    save_xml_to_file(dom, svg_updated)


if __name__ == "__main__":
    path_to_archimate = sys.argv[1]
    path_to_svg_source = sys.argv[2]
    path_to_svg_destination = sys.argv[3]

    path_to_javascript = "svg-dynamic-tooltip.js-svg"

    add_javascript(path_to_svg_source, path_to_svg_destination, path_to_javascript)
    archimate_description = archi_elements(path_to_archimate)
    update_svg_elements(path_to_svg_destination, archimate_description, path_to_svg_destination)
