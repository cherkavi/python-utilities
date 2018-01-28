from lxml import html

page = html.parse("http://www.mctrek.de/bekleidung-unisex-herren/wintersport-skibekleidung/jacken/icepeak-kurt-wintersportjacke-herren_4047336")
# list_of_size = page.xpath('//*[@id="wk_addItem"]/option/text()')
# print(list_of_size)

list_of_size = page.xpath('//*[@id="wk_addItem"]')
print(list_of_size[0].value_options)
