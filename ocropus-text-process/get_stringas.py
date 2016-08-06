import os,os.path
import re
import numpy
import unicodedata
import sys
import chars


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
        return re.sub(ur'[^A-Za-z]','',s)
    if kind=="digits":
        return re.sub(ur'[^0-9]','',s)
    if kind=="lnc":
        s = s.upper()
        return re.sub(ur'[^A-Z]','',s)
    raise BadInput("unknown normalization: "+kind)

print project_text("1233 33 *** JdJAD",sys.argv[1])
