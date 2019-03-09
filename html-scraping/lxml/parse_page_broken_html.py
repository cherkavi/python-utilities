from lxml import html
import requests

page = requests.get("http://spys.one/free-proxy-list/UA/")
tree = html.fromstring(page.content)
# for XPath remove all "<tbody>" elements 
addresses = tree.xpath("/html/body/table[2]/tr[4]/td/table/tr[*]/td[1]/font[2]")
for each_address in addresses:
    print(each_address.text)
    print(each_address.getchildren()[0].text)
