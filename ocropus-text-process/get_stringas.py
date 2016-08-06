# -*- encoding: utf-8 -*-
import os,os.path
import re
import numpy
import unicodedata
import sys
import chars
import numpy as np

replacements = chars.replacements
def normalize_text(s):
    """Apply standard Unicode normalizations for OCR.
    This eliminates common ambiguities and weird unicode
    characters."""
    s = unicode(s)
    s = unicodedata.normalize('NFC',s)
    s = re.sub(ur'\s+(?u)',' ',s)
    s = re.sub(ur'\n(?u)','',s)
    s = re.sub(ur'^\s+(?u)','',s)
    s = re.sub(ur'\s+$(?u)','',s)
    for m,r in replacements:
        s = re.sub(unicode(m),unicode(r),s)
    return s

def project_text(s,kind="exact"):
    """Project text onto a smaller subset of characters
    for comparison."""
    s=re.sub(r'[^\x00-\x7F]+',' ',s)
    s = normalize_text(s)
    s = re.sub(ur'( *[.] *){4,}',u'....',s) # dot rows
    s = re.sub(ur'[~_]',u'',s) # dot rows
    if kind=="exact":
        return s
    if kind=="nospace":
        return re.sub(ur'\s','',s)
    if kind=="spletdig":
        return re.sub(ur'[^A-Za-z0-9 ]','',s)
    if kind=="letdig":
        return re.sub(ur'[^A-Za-z0-9]','',s)
    if kind=="letters":
        return re.sub(ur'[^A-Za-z]',' ',s)
    if kind=="digits":
        return re.sub(ur'[^0-9]','',s)
    if kind=="lnc":
        s = s.upper()
        return re.sub(ur'[^A-Z]','',s)
    raise BadInput("unknown normalization: "+kind)

def string_with_lessNumbers(st):
        num=[]
        for f in st:
           num.append(len(project_text(f,'digits')))
        index=np.argmin(num)
        return st[index]

#input is list of strings output will be list of strings with least number of digits --inp=['ada','12132','ada3']
def string_contain_lessNumbers(st):
        
        num=[]
        out=[]
        for f in st:
           num.append(len(project_text(f,'digits')))
           if len(project_text(f,'digits'))==0:
                 out.append(f)
        if len(st)==0:
           index=np.argmin(num)
           out.append(st[index])
        return out

def countSyllables(word):
    vowels = "aeiouy"
    numVowels = 0
    lastWasVowel = False
    for wc in word:
        foundVowel = False
        for v in vowels:
            if v == wc:
              if not lastWasVowel: numVowels+=1   #don't count diphthongs
              foundVowel = lastWasVowel = True
              break
        if not foundVowel:  #If full cycle and no vowel found, set lastWasVowel to false
            lastWasVowel = False
    if len(word) > 2 and word[-2:] == "es": #Remove es - it's "usually" silent (?)
        numVowels-=1
    elif len(word) > 1 and word[-1:] == "e":    #remove silent e
        numVowels-=1
    return numVowels

def get_valid_str(sent):
    out_st=''
    st=sent.split(' ')
    vowels = "aeiouy"
    numVowels = 0
    lastWasVowel = False
    for f in st:
     cnt=0
     for wc in f:
        for v in vowels:
           if v == wc:
               cnt=cnt+1
     if cnt!=0:
        if float(len(f)/cnt)<1.0:
           out_st=out_st+f+' '
    return out_st
 




