# import file/module not in your "classpath"
# import remote file from classpath

##### approach 1.1
import sys
# insert at 1, 0 is the script path (or '' in REPL)
# sys.path.insert(1, '/path/to/application/app/folder')
sys.path.append('/path/to/application/app/folder')
import destination_file

##### approach 1.2
import sys
path_to_site_packages="/opt/homebrew/lib/python2.7/site-packages"  # Replace this with the place you installed facebookads using pip
sys.path.append(path_to_site_packages)
sys.path.append(f"{path_to_site_packages}/facebook_business-3.0.0-py2.7.egg-info")
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

##### approach 2
# from full.path.to.python.folder import func_name
