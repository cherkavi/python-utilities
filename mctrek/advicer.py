from lxml import html

start_page = "http://www.mctrek.de/shop/sale?hersteller[]=Jack+Wolfskin&suchevon="

# list_of_size = page.xpath('//*[@id="wk_addItem"]/option/text()')
# print(list_of_size)
# list_of_size = 
# print(list_of_size[0].value_options)


def next_page_generator():
    index = 0
    while True:
        yield start_page + str(index*24)
        index = index+1

next_page = next_page_generator()
html_url = next_page.next()
print(html_url)
page = html.parse(html_url)
# found_elements = page.xpath('/html/body/div[9]/div/div[2]/div[2]/div[6]')
found_elements = page.xpath('/html/body/div[9]/div/div/div')
print(dir(found_elements[0]))
print(found_elements[0].attrib)
for element in found_elements[0].getchildren():
    print (">>>> %s   %s" % (element.tag, element.attrib))
print(found_elements)
