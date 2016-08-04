'''
import xml.etree.cElementTree as ET
import glob,cv2

#def create_image_xml(img_name,w,h,d,class_name,xmin,ymin,xmax,ymax,name_im):
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
#os.system('rm output/*')
root1 = ET.Element("dataset")
name_=ET.SubElement(root1,"name").text="imglab dataset"
comment_=ET.SubElement(root1,"comment").text="Created by imglab tool."
images_=ET.SubElement(root1, "images")
with open('empt.txt','r') as data:
   content=data.readlines()
files=[]
for f in content:
   files.append(f.strip())

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
    img=cv2.imread(f)
    
    for j in root.iter('annotation'):
	       image_name='output/'+j[1].text+'.jpg'
               if image_name in files:
                   print "yes"
               else:
	           for k in j.iter('object'):
                       #print f
                       if k[0].text=='accno_dlib':
                           for m in k.iter('bndbox'):
                            #print "yyy"
                                x1=int(m[0].text)
		                y1=int(m[1].text)
		                x2=int(m[2].text)
		                y2=int(m[3].text)
                                print x1,"ll"
                                im_part=img[y1:y2,x1:x2]
                                #im_part_res=cv2.resize(im_part,(im_part.shape[1]*3,im_part.shape[0]*3))
                                cv2.imwrite("out.jpg",im_part)
                                #image_=ET.SubElement(images_, "image", file=image_name)
                                #box_=ET.SubElement(image_, "box",top=str(y1),left=str(x1),width=str(abs(x2-x1)),height=str(abs(y2-y1)))
                                
                                #print "output"+f.split('cheque_seg_output_with_xml')[1]
                       if k[0].text=='accno_seg':
                           for m in k.iter('bndbox'):
                            #print "yyy"
                                x1_s=int(m[0].text)
		                y1_s=int(m[1].text)
		                x2_s=int(m[2].text)
		                y2_s=int(m[3].text)
                                x1_r=3*abs(x1_s-x1)
                                y1_r=3*abs(y1_s-y1)
                                x2_r=3*abs(x2_s-x1)
                                y2_r=3*abs(y2_s-y1)
                                im_part_res=cv2.resize(im_part,(im_part.shape[1]*3,im_part.shape[0]*3))
                                sm=im_part_res[y1_r:y2_r,x1_r:x2_r]
                                f_name='acc_no_dlib_resized_small_part_train/'+f.split('/')[-1]
                                cv2.imwrite(f_name,im_part_res)
                                cv2.imwrite('parts/'+f.split('/')[-1],sm)
                                image_=ET.SubElement(images_, "image", file=f_name)
                                box_=ET.SubElement(image_, "box",top=str(y1_r),left=str(x1_r),width=str(abs(x2_r-x1_r)),height=str(abs(y2_r-y1_r)))
                                
                                
  except:
       pass
tree = ET.ElementTree(root1)
tree.write("acc2_small_part_dlib.xml")
