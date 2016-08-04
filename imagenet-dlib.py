import glob
import xml.etree.ElementTree as ET
import numpy,os,cv2,glob
from time import gmtime,strftime
from datetime import datetime
'''
root = ET.Element("dataset")
name_=ET.SubElement(root,"name").text="imglab dataset"
comment_=ET.SubElement(root,"comment").text="Created by imglab tool."
images_=ET.SubElement(root, "images")
image_=ET.SubElement(images_, "image", file="5-02-2016-23-26-181_cc-340064.jpg")
box_=ET.SubElement(image_, "box",top="3444",left="232",width="3444",height="23ss2")
tree = ET.ElementTree(root)
tree.write("out.xml")
'''

import glob
import xml.etree.ElementTree as ET
import numpy,os,cv2,glob
from time import gmtime,strftime
from datetime import datetime
root1 = ET.Element("dataset")
name_=ET.SubElement(root1,"name").text="imglab dataset"
comment_=ET.SubElement(root1,"comment").text="Created by imglab tool."
images_=ET.SubElement(root1, "images")

cnt=0
for f in glob.glob("hdfc/*.jpg"):
  try:
    try:
      f_name=f.split('.jpg_warped.jpg')[0]+'.jpg_warped.xml'

      tree = ET.parse(f_name)
      root=tree.getroot()
    except:
      f_name=f.split('.jpg_warped.jpg')[0]+'.jpg_warped'
      tree = ET.parse(f_name)
      root=tree.getroot()
    for j in root.iter('annotation'):
	       #print j[1].text
	       for k in j.iter('object'):
                   #for l in k.iter('name'):
                       if k[0].text=='accno_dlib':
                           for m in k.iter('bndbox'):
                                cnt=cnt+1
                                image_=ET.SubElement(images_, "image", file=f)
                                x1=int(m[0].text)
		                y1=int(m[1].text)
		                x2=int(m[2].text)
		                y2=int(m[3].text)
                                box_=ET.SubElement(image_, "box",top=str(y1),left=str(x1),width=str(abs(x2-x1)),height=str(abs(y2-y1)))
  except:
       pass

tree = ET.ElementTree(root1)
tree.write("out.xml")
