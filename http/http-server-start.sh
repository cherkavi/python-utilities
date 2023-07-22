# simple http server with cgi ( script execution ) ability

# https://realpython.com/python-http-server/

# start simple http web server with list of files inside
python3 -m http.server 9090
x-www-broser localhost:9090

# or start with more customized version
nohup python3 http-server.py &

# start with /cgi-bin folder processing
python3 -m http.server --cgi 9090
