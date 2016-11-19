#!/usr/bin/python
import sys
import lxml.etree as ET

if len(sys.argv) < 3:
    print "syntax: %s input.XML output.A2L" % (sys.argv[0])
    sys.exit()

dom = ET.parse(sys.argv[1])
for element in dom.iter():
    element.tail = None
xslt = ET.parse("a2l.xslt")
transform = ET.XSLT(xslt)
newdom = transform(dom)
f = open(sys.argv[2], "w")
f.write(str(newdom))
f.close()
#print(ET.tostring(newdom, pretty_print=True))
