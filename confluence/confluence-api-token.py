# https://atlassian-python-api.readthedocs.io/confluence.html
# pip3 install atlassian-python-api
from atlassian import Confluence

URL='https://ubsgroup.com/confluence'
PAGE='https://ubsgroup.com/confluence/display/OOO/Data+Model'
# confluence.get_space("OOO")
PAGE_SPACE="OOO"
# confluence.get_page_by_title(PAGE_SPACE, "OOO -Data Model")["id"]
PAGE_ID='5555110754'
# confluence.get_parent_content_id(PAGE_ID)
PAGE_ID_PARENT='5555110751'
# confluence token https://ubsgroup.com/confluence/plugins/personalaccesstokens/usertokens.action
TOKEN='my secret token from'
confluence = Confluence(url=URL, token=TOKEN)

# get all spaces
spaces_response: dict=confluence.get_all_spaces() 
spaces: list = spaces_response["results"]
# elements = [each_space for each_space in spaces if each_space["name"].startswith("central")]
elements = [each_space for each_space in spaces if each_space["key"].startswith(PAGE_SPACE)]
print(elements)

# get page by id
confluence.get_page_by_id(PAGE_ID)

# create page 
confluence.create_page(PAGE_SPACE, "remove_me", "some text inside body", PAGE_ID_PARENT)
# 
confluence.get_page_by_id("5555722821")
confluence.remove_page("5555722821")

create_result = confluence.create_page(space="AD", title="remove me", body="checking confluence api")
print(create_result)
