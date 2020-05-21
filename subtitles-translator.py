# simple application for translate all Disney subtitles (JS filter "seg") 
# from DEutsch to RUssian
# 
# file example
# 00:01:06.691 --> 00:01:09.069 line:14.96%,start
# 20 Jahre zuvor
#
# 00:01:11.196 --> 00:01:15.992
# Was machen wir nur hier? Kannst du sie
# nicht einfach dazu bringen, Ja zu sagen?
# 
# 00:01:16.076 --> 00:01:18.495 line:85.04%,end
# Ich kÃ¶nnte, aber das ist nicht meine Art.


import sys
import subprocess
from time import sleep

def clear_binary_line(b_line):
    return b_line.decode('utf-8').rstrip()


buffer = ""

for line in sys.stdin:
    prepared_line = line.strip()
    if len(prepared_line)==0:
        continue
    
    remove_marker = prepared_line.find("-->")    
    if remove_marker > 0:
        sleep(5)
        translation = subprocess.check_output(["trans", "--no-warn", "-source", "de","-target","ru", "-brief", buffer])
        print(buffer, "   ")
        print("```",clear_binary_line(translation),"```")
        print(line[0:remove_marker]+"  \n---")
        buffer = ""
    else:        
        buffer = buffer + " " + prepared_line
