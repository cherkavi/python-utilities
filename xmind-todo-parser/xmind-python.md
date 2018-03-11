git clone https://github.com/xmindltd/xmind-sdk-python.git
cd xmind-sdk-python
python setup.py install


#-*- coding: utf-8 -*-
import xmind
from xmind.core import workbook,saver
from xmind.core.topic import TopicElement

workbook = xmind.load("central.xmind")
sheet = workbook.getPrimarySheet()
topic = sheet.getRootTopic()
topic.getTitle()
topic.getMarkers()
topic.getSubTopics()
topic.getSubTopics()[0].getNotes()
topic.getSubTopics()[0].getNotes().getContent()


https://github.com/xmindltd/xmind-sdk-python
https://github.com/xmindltd/xmind-sdk-python/blob/master/example.py

topic.getMarkers()[0].getMarkerId().name


https://bitbucket.org/Mekk/mekk.xmind/
