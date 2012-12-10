#!/usr/bin/python

import sys

def toXML(a):
    return a.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") 

if __name__ == "__main__":
   if len(sys.argv) != 3:
      print "Usage: run.py <fichero_marc> <fichero_xml>"
      sys.exit(-1)
   
   f = open(sys.argv[2], "w")
   err = open("%s.error" % sys.argv[2], "w")
   
   f.write("""<?xml version="1.0" encoding="utf-8" ?>\n""")
   f.write("""<marc:collection xmlns:marc="http://www.loc.gov/MARC21/slim" 
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                    xsi:schemaLocation="http://www.loc.gov/MARC21/slim http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">\n""")
   
   content = open(sys.argv[1], "r").readlines()[0]
   
   while True:
       try:
          lengthLine = int(content[:5])
       except:
          break
   
       r = content[:lengthLine]
   
       try:
          f.write("""%s<marc:record>\n""" % (" "*2))
          f.write("""%s<marc:leader>%s</marc:leader>\n"""  % (" "*4, r[:24]))
   
          index = 0
   
          for d in r.split("\x1e")[1:-1]:
             if int(r[24:][(12*index):(12*index)+2]) == 0:
                controlfield = d
                f.write("""%s<marc:controlfield tag="%s">%s</marc:controlfield>\n"""  % (" "*4, r[24:][(12*index):(12*index)+3], controlfield))
   
             elif len(d) > 0:
                f.write("""%s<marc:datafield tag="%s" ind1="%s" ind2="%s">\n""" % (" "*4, r[24:][(12*index):(12*index)+3],d[0],d[1]))
   
                for s in d.split("\x1f")[1:]:
                    if len(s) > 0:
                       f.write("""%s<marc:subfield code="%s">%s</marc:subfield>\n""" % (" "*6, s[0],toXML(s[1:])))
      
                f.write("""%s</marc:datafield>\n""" % (" "*4))
   
             index = index + 1
   
          f.write("""%s</marc:record>\n""" % (" "*2))
       except Exception, msg:
          err.write("%s - %s\n" % (r, msg))
   
       content = content[lengthLine:]
       
   
   f.write("""</marc:collection>\n""")
   f.close()
   err.close()
