# maintenance page
# html server read parameters and path example
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class CustomRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        ## Access the captured path
        # parsed_url = urlparse(self.path)
        # path = parsed_url.path
        # print("Path:", path)

        ## Access query parameters
        # query_params = parse_qs(parsed_url.query)
        # print("Query parameters:", query_params)

        ## Print remote_addr of the client
        self.wfile.write(f"remote_addr:{self.client_address[0]} <br />\n".encode("utf-8"))
        
        ## Access to headers, print http headers from GET request
        self.send_response(200)
        
        self.send_header("Content-type", "text/html"); self.end_headers() # curl: (1) Received HTTP/0.9 when not allowed
        for each_header in self.headers:
            self.wfile.write(f"{each_header}   {self.headers[each_header]} \n".encode("utf-8"))

        # send 503
        # self.send_response(503)
        # self.send_header('Content-type', 'text/html')
        # self.end_headers()
        # self.wfile.write(b'<h1>Dear Users,<br><br>Due to platform issues, [application] will be out of order till the problem is solved.<br><br>Best Regards,<br>Team</h1>')

if __name__ == '__main__':
    server_address = ('', 9191)
    httpd = HTTPServer(server_address, CustomRequestHandler)
    print('Server is running on http://localhost:9191')
    httpd.serve_forever()
