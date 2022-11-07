# pip install webb

from webb import webb

http_address = "http://mail.ru"

webb.get_ip(http_address)
webb.get_whois_data(http_address)
webb.ping(http_address)
webb.traceroute(http_address)
webb.clean_page( webb.download_page(http_address) )

# webb.web_crawl(http_address)