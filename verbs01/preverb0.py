#-*- coding:utf-8 -*-
"""preverb0.py for CCS
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline
import transcoder
transcoder.transcoder_set_dir('transcoder')

class Entry(object):
 Ldict = {}
 def __init__(self,lines,linenum1,linenum2):
  # linenum1,2 are int
  self.metaline = lines[0]
  self.lend = lines[-1]  # the <LEND> line
  self.datalines = lines[1:-1]  # the non-meta lines
  # parse the meta line into a dictionary
  #self.meta = Hwmeta(self.metaline)
  self.metad = parseheadline(self.metaline)
  self.linenum1 = linenum1
  self.linenum2 = linenum2
  #L = self.meta.L
  L = self.metad['L']
  if L in self.Ldict:
   print("Entry init error: duplicate L",L,linenum1)
   exit(1)
  self.Ldict[L] = self
  #  extra attributes
  self.marked = False # from a filter of markup associated with verbs
  self.marks = []  # verb markup markers, in order found, if any
  
def init_entries(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 recs=[]  # list of Entry objects
 inentry = False  
 idx1 = None
 idx2 = None
 for idx,line in enumerate(lines):
  if inentry:
   if line.startswith('<LEND>'):
    idx2 = idx
    entrylines = lines[idx1:idx2+1]
    linenum1 = idx1 + 1
    linenum2 = idx2 + 1
    entry = Entry(entrylines,linenum1,linenum2)
    recs.append(entry)
    # prepare for next entry
    idx1 = None
    idx2 = None
    inentry = False
   elif line.startswith('<L>'):  # error
    print('init_entries Error 1. Not expecting <L>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <LEND>
    continue
  else:
   # inentry = False. Looking for '<L>'
   if line.startswith('<L>'):
    idx1 = idx
    inentry = True
   elif line.startswith('<LEND>'): # error
    print('init_entries Error 2. Not expecting <LEND>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <L>
    continue
 # when all lines are read, we should have inentry = False
 if inentry:
  print('init_entries Error 3. Last entry not closed')
  print('Open entry starts at line',idx1+1)
  exit(1)

 print(len(lines),"lines read from",filein)
 print(len(recs),"entries found")
 return recs

class MWVerb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.k1,self.L,self.cat,self.cps,self.parse = line.split(':')
  self.used = False

def init_mwverbs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [MWVerb(x) for x in f]
 print(len(recs),"mwverbs read from",filein)
 #recs = [r for r in recs if r.cat == 'verb']
 #recs = [r for r in recs if r.cat in ['root','genuineroot']]
 recs = [r for r in recs if r.cat == 'preverb']
 print(len(recs),"verbs returned from mwverbs")
 d = {}
 for rec in recs:
  k1 = rec.k1
  if k1 in d:
   print('init_mwverbs: Unexpected duplicate',k1)
  d[k1] = rec
 return recs,d


def unused_mark_entries_verb(entries,pwnonverbsd):
 for entry in entries:
  # first exclude known non-verbs
  k1 = entry.metad['k1']
  #if k1 in pwnonverbsd:
  # continue
  # might be a verb. look for upasarga pattern
  marks = []
  for iline,line in enumerate(entry.datalines):
   for m in re.finditer(u'<div n="p">—? *{#(.*?)#}',line):
    if entry.metad['L'] == '14791':print('check',m.group(0))
    upasarga = m.group(1)
    # add upasarga to the list of marks
    marks.append(upasarga)
    
  if len(marks) == 0:
   continue
  continue  # skip thi
  # remove cases where ONLY Desid.|Intens.|Caus. is present in marks
  marks = [x for x in marks if x not in ['Desid.','Intens.','Caus.']]
  if len(marks) > 0:
   """ Consider cases like 
     {#*marImfja#}¦ <lex>Adj.</lex> vom <ab>Intens.</ab> von {#marj#}.
    which should NOT be marked as verb
   """
   isverb = True  # tentatively
   line = entry.datalines[0]
   if re.search(r'¦ *<lex>',line):
    print(entry.metad['k1'],entry.metad['L'],' NOT A VERB')
    isverb = False #  No, mistaken identity!
   if isverb:
    entry.marked = True
    entry.marks = marks

def merge_marked_entries(entries):
 d = {}
 keys = []
 for entry in entries:
  if not entry.marked:
   continue
  k1 = entry.metad['k1']
  if k1 not in d:
   d[k1] = []
   keys.append(k1)
  d[k1].append(entry)
 entrylists = []
 for k1 in keys:
  entrylists.append(d[k1])
 return entrylists


def yesno(flag):
 if flag:
  return 'yes'
 else:
  return 'no'

def dump_entry(entry):
 outarr = [entry.metaline] + entry.datalines
 outarr = outarr + [';']
 return '\n'.join(outarr)
 
def write(fileout,recs,tranout='slp1'):
 tranin = 'slp1'
 def transcode(x):
  return transcoder.transcoder_processString(x,tranin,tranout)
 n = 0
 nyes = 0
 nno = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for irec,rec in enumerate(recs):
   entry = rec.entry
   upasargas = rec.upasargas
   k1 = entry.metad['k1']  
   L =  entry.metad['L']
   k2 = entry.metad['k2']
   ustring = ','.join(upasargas)
   out1 = ';; Case %04d: L=%s, k1=%s, #upasargas=%s, upasargas=%s' %(
    irec+1,L,transcode(k1),len(upasargas),ustring)
   f.write(out1+'\n')
   if False:  # for debugging
    s = dump_entry(entry)
    print(s)
    print('upas=',ustring)
    print()
   n = n + 1
 print(n,"records written to",fileout)
 print(nyes,"mwpreverb spellings found")
 print(nno,"mwpreverb spellings NOT found")

class Ccsverb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), code=(.*), mw=(.*)$',line)
  self.L,self.k1,self.k2,self.code,self.mw = m.group(1),m.group(2),m.group(3),m.group(4),m.group(5)
  self.upasargas = []
  self.entry = None
  self.preverbs = []
  self.mwpreverbs = []
  self.mwpreverbs_found = []
  self.mwpreverbs_parse = []

def init_ccsverbs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Ccsverb(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

def find_entries(recs,entries):
 # dictionary for entries
 d = {}
 for entry in entries:
  d[entry.metad['L']]= entry
 # 
 for irec,rec in enumerate(recs):
  L = rec.L
  try:
   entry = d[L]
   rec.entry = entry
   entry.marked = True
  except:
   print('find_entries. bad L=',rec.L)
   print('record # ',irec+1)
   print('  line = ',rec.line)
   exit(1)

def parse_sanskrit_string(x):
 # SLP1 coding of Sanskrit
 # remove accents 
 x = re.sub(r'[/\^]','',x)
 # remove 'missing' character
 x = re.sub(r'°','',x)
 # remove page breaks
 x = re.sub(r'\[Page.*?\]',' ',x)
 # remove long dash
 x = re.sub(r'—','',x)
 # remove hyphen
 x = re.sub(r'-','',x)
 # return strings of alphabetical characters
 a = re.findall(r'\w+',x)
 return a

def find_sanskrit_words(text):
 a = []
 # skip headword and first inflected form
 x = re.sub(r'^.*¦','',text)
 """
 if x == text:
  print('chk:\nx=%s\ntext=%s'%(x,text))
  exit(1)
 else:
  print('chk1:\nx=%s\nx=%s'%(x,text))
  exit(1)
 """
 # iterate over Devanagari text strings
 for m in re.finditer(r'{#(.*?)#}',x):
  b = parse_sanskrit_string(m.group(1)) # list of 'distinct' words
  a = a + b
 return a

def find_upasargas(recs,knownupas):
 nrec = 0
 nupa = 0
 for rec in recs:
  entry = rec.entry
  upasargas = []
  L = entry.metad['L']
  k1 = entry.metad['k1'] 
  text = ' '.join(entry.datalines)
  sanskrit_words = find_sanskrit_words(text)
  upasargas = [x for x in sanskrit_words if x in knownupas]
  if False:
   print(L,k1,' , '.join(upasargas))
   continue
  rec.upasargas = upasargas
  if len(upasargas) > 0:
   nrec = nrec + 1
   nupa = nupa + len(upasargas)

 print(nupa,"upasargas found in",nrec,"entries")

def non_verb_upasargas(entries):
 nrec = 0
 nupa = 0
 ans = []
 for entry in entries:
  if entry.marked:  # skip verb entries
   continue
  upasargas = []
  lines = entry.datalines
  for iline,line in enumerate(lines):
   m = re.search(u'<div n="p">— {#([a-zA-Z]+)#}',line)
   if m:
    upasarga = m.group(1)
    upasargas.append(upasarga)
  #rec.upasargas = upasargas
  if len(upasargas) > 0:
   nrec = nrec + 1
   nupa = nupa + len(upasargas)
   entry.upasargas = upasargas
   ans.append(entry)

 print(nupa,"upasargas found in",nrec,"non-verb entries")
 fileout = 'preverb1_tempupa.txt'
 with codecs.open(fileout,'w','utf-8') as f:
  for ientry,entry in enumerate(ans):
   L = entry.metad['L']
   k1 = entry.metad['k1']
   upasargas = entry.upasargas
   out = ';; Case %04d: L=%s, k1=%s, #upasargas=%s' %(ientry+1,L,k1,len(upasargas))
   f.write(out+'\n')
  print(len(ans),"records written to",fileout)

sandhimap = {
 ('i','a'):'ya',
 ('i','A'):'yA',
 ('i','i'):'I',
 ('i','I'):'I',
 ('i','u'):'yu',
 ('i','U'):'yU',
 ('i','f'):'yf',
 ('i','F'):'yF',
 ('i','e'):'ye',
 ('i','E'):'yE',
 ('i','o'):'yo',
 ('i','O'):'yO',

 ('u','a'):'va',
 ('u','A'):'vA',
 ('u','i'):'vi',
 ('u','I'):'vI',
 ('u','u'):'U',
 ('u','U'):'U',
 ('u','f'):'vf',
 ('u','F'):'vF',
 ('u','e'):'ve',
 ('u','E'):'vE',
 ('u','o'):'vo',
 ('u','O'):'vO',

 ('a','a'):'A',
 ('a','A'):'A',
 ('A','a'):'A',
 ('A','A'):'A',
 
 ('a','i'):'e',
 ('A','i'):'e',
 ('a','I'):'e',
 ('A','I'):'e',
 
 ('a','u'):'o',
 ('A','u'):'o',
 ('a','U'):'o',
 ('A','U'):'o',
 
 ('a','f'):'Ar',
 ('A','f'):'Ar',
 ('a','e'):'e',
 ('d','s'):'ts',
 ('a','C'):'acC', # pra+Cad = pracCad
 ('A','C'):'AcC', # A + Cid = AcCid
 ('i','C'):'icC',
 ('d','q'):'qq',  # ud + qI
 ('d','k'):'tk',
 ('d','K'):'tK',
 ('d','c'):'tc',
 ('d','C'):'tC',
 ('d','w'):'tw',
 ('d','W'):'tW',
 ('d','t'):'tt',
 ('d','T'):'tT',
 ('d','p'):'tp',
 ('d','P'):'tP',
 ('d','s'):'ts',
 ('d','n'):'nn',

 ('i','st'):'izw',
 ('s','h'):'rh', # nis + han -> nirhan
 ('m','s'):'Ms', # sam + saYj -> saMsaYj
 ('m','S'):'MS',
 ('m','k'):'Mk',
 ('m','K'):'MK',
 ('m','c'):'Mc',
 ('m','C'):'MC',
 ('m','j'):'Mj',
 ('m','J'):'MJ',

 ('m','w'):'Mw',
 ('m','W'):'MW',
 ('m','t'):'Mt',
 ('m','T'):'MT',
 ('m','p'):'Mp',
 ('m','P'):'MP',

 ('m','v'):'Mv',
 ('m','l'):'Ml',
 ('m','r'):'Mr',
 ('m','y'):'My',
 ('m','n'):'Mn',
 
 ('s','k'):'zk', # nis + kf -> nizkf
 ('s','g'):'rg',
 ('s','G'):'rG',
 ('s','c'):'Sc',
 ('s','j'):'rj',
 ('s','q'):'rq',
 ('s','d'):'rd',
 ('s','D'):'rD',
 ('s','b'):'rb',
 ('s','B'):'rB',
 ('s','m'):'rm',
 ('s','n'):'rn',
 ('s','y'):'ry',
 ('s','r'):'rr',
 ('s','l'):'rl',
 ('s','v'):'rv',

 ('r','c'):'Sc',
 ('r','C'):'SC',
 ('d','l'):'ll',
 ('d','h'):'dD',
 ('d','S'):'cC',
 ('d','m'):'nm',

}
def join_prefix_verb(pfx,root):
 if pfx.endswith('ud') and (root == 'sTA'):
  return pfx[0:-2] + 'ut' + 'TA'  # ud + sTA = utTA
 if (pfx == 'saMpra') and (root in ['nad','nam','naS']):
  pfx = 'sampra'
  root = 'R' + root[1:]
  return pfx + root
 if (pfx == 'pra') and (root == 'nakz'):
  return 'pranakz' # odd, since mw has aBipraRakz
 pfx1,pfx2 = (pfx[0:-1],pfx[-1])
 root1,root2 = (root[0],root[1:])
 if (pfx2,root1) in sandhimap:
  return pfx1 + sandhimap[(pfx2,root1)] + root2
 if len(root) > 1:
  root1,root2 = (root[0:2],root[2:])
  if (pfx2,root1) in sandhimap:
   return pfx1 + sandhimap[(pfx2,root1)] + root2
 if root == 'i':
  if pfx == 'dus':
   return 'duri'
  if pfx == 'nis':
   return 'niri'
 if 'saMpra' in pfx:
  pfx = pfx.replace('saMpra','sampra')
  return pfx + root
 if  pfx.endswith(('pari','pra')) and root.startswith('n'):
  return pfx + 'R' + root[1:]  # pra + nad -> praRad
 if pfx.endswith('nis') and root.startswith(('a','I','u','U')):
  pfx = pfx.replace('nis','nir')
  return pfx + root
 ans = pfx + root
 d = {'duscar':'duScar'}
  
 if ans in d:
  ans = d[ans]
 return ans
mwpreverb_adjustments = {}

def adjust_mwpreverb(preverb,mwdict):
 #if preverb == 'sampranI':print('adjust_mwpreverb 1',preverb)
 if preverb in mwpreverb_adjustments:
  x = mwpreverb_adjustments[preverb]
  if x in mwdict:
   return x
 #if preverb == 'aByasUy':print('adjust_mwpreverb 2',preverb)
 if preverb in mwdict:
  return preverb # no adjustment needed
 if re.search(r'sa[mM]p',preverb):
  x = preverb.replace('saMp','samp')
  if x in mwdict:
   return x
  x = preverb.replace('samp','saMp')
  if x in mwdict:
   return x
  #return preverb
 if re.search(r'.*r.*n$',preverb):  #parAn -> paraR, etc
  x = preverb[0:-1]+'R'
  if x in mwdict:
   return x
 if re.search(r'r.R',preverb):
  x = re.sub(r'r(.)R',r'r\1n',preverb)
  if x in mwdict:
   return x

 if 'samh' in preverb:
  x = preverb.replace('samh','saMh')
  if x in mwdict:
   return x
 if 'utc' in preverb:
  x = preverb.replace('utc','ucc')
  if x in mwdict:
   return x
 if 'utC' in preverb:
  x = preverb.replace('utC','ucC')
  if x in mwdict:
   return x
 if 'udj' in preverb:
  x = preverb.replace('udj','ujj')
  if x in mwdict:
   return x
 if preverb.endswith('isad'):
  x = re.sub(r'isad$','izad',preverb)
  if x in mwdict:
   return x
 if re.search(r'is',preverb):
  x = re.sub(r'is',r'iz',preverb)
  if x in mwdict:
   return x
 if re.search(r'isT',preverb):
  x = re.sub(r'isT',r'izW',preverb)
  if x in mwdict:
   return x
 if re.search(r'us',preverb):
  x = re.sub(r'us',r'uz',preverb)
  if x in mwdict:
   return x
 if re.search(r'usT',preverb):
  x = re.sub(r'usT',r'uzW',preverb)
  if x in mwdict:
   return x
 if re.search(r'niss',preverb):
  x = re.sub(r'niss',r'niHs',preverb)
  if x in mwdict:
   return x
 if re.search(r'nisS',preverb):
  x = re.sub(r'nisS',r'niHS',preverb)
  if x in mwdict:
   return x
 if re.search(r'niszW',preverb):
  x = re.sub(r'niszW',r'niHzW',preverb)
  if x in mwdict:
   return x
 if re.search(r'nisv',preverb):
  x = re.sub(r'nisv',r'nirv',preverb)
  if x in mwdict:
   return x
 if re.search(r'udm',preverb):
  x = re.sub(r'udm',r'unm',preverb)
  if x in mwdict:
   return x
 if re.search(r'udh',preverb):
  x = re.sub(r'udh',r'udD',preverb)
  if x in mwdict:
   return x
 if re.search(r'sam[gGjJdDbByrlvSzs]',preverb):
  x = re.sub(r'sam([gGjJdDbByrlvSzs])',r'saM\1',preverb)
  if x in mwdict:
   return x
 if re.search(r'antar',preverb):
  x = re.sub(r'antar',r'antaH',preverb)
  if x in mwdict:
   return x
 if re.search(r'ra[rs]',preverb):
  x = re.sub(r'ra[rs]',r'ro',preverb)
  if x in mwdict:
   return x
 if re.search(r'acCa',preverb):
  x = re.sub(r'acCa',r'acCA',preverb)
  if x in mwdict:
   return x
 if re.search(r'paryAn',preverb):
  x = re.sub(r'paryAn',r'paryAR',preverb)
  if x in mwdict:
   return x
 if re.search(r'nirn',preverb):
  x = re.sub(r'nirn',r'nirR',preverb)
  if x in mwdict:
   return x
 if re.search(r'parAn',preverb):
  x = re.sub(r'parAn',r'parAR',preverb)
  if x in mwdict:
   return x
 if re.search(r'pran',preverb):
  x = re.sub(r'pran',r'praR',preverb)
  print('chk:',preverb,x)
  if x in mwdict:
   return x
 if re.search(r'st',preverb):
  x = re.sub(r'st',r'zw',preverb)
  if x in mwdict:
   return x
 if re.search(r'sT',preverb):
  x = re.sub(r'sT',r'zW',preverb)
  if x in mwdict:
   return x
 if re.search(r'zw',preverb):
  x = re.sub(r'zw',r'st',preverb)
  if x in mwdict:
   return x
 if re.search(r'zW',preverb):
  x = re.sub(r'zW',r'sT',preverb)
  if x in mwdict:
   return x
 if re.search(r'tst',preverb):
  x = re.sub(r'tst',r'tt',preverb)
  if x in mwdict:
   return x
 if re.search(r'tsT',preverb):
  x = re.sub(r'tsT',r'tT',preverb)
  if x in mwdict:
   return x
 if preverb == 'nissTA':
  x = 'niHzWA'
  if x in mwdict:
   return x
 if preverb == 'nisnA':
  x = 'nizRA'
  if x in mwdict:
   return x
 if preverb == 'saMparisvaYj':
  x = 'samparizvaYj'
  if x in mwdict:
   return x
 if preverb.endswith(('kf','df','pf')):
  x = preverb[0:-1]+'F'
  if x in mwdict:
   return x
 
 return preverb

def join_upasargas(recs,mwpreverbs_dict):
 for rec in recs:
  upasargas = rec.upasargas
  if len(upasargas) == 0:
   continue
  if rec.mw == '?':
   print(len(upasargas),'upasargas, but no mw root',rec.line)
   continue
  
  #mwrec = rec.mwrec
  k1 = rec.k1
  kmw = rec.mw
  rec.mwpreverbs = []
  rec.preverbs = []
  rec.mwpreverbs_found = []
  rec.mwpreverbs_parse = []
  for u in upasargas:
   pwg_preverb = join_prefix_verb(u,k1)
   if False and (k1 == 'asUy'):
    print('pwg',u,k1,pwg_preverb)
   rec.preverbs.append(pwg_preverb)
   mw_preverb0 = join_prefix_verb(u,kmw)
   mw_preverb = adjust_mwpreverb(mw_preverb0,mwpreverbs_dict)
   if False and (k1 == 'asUy'):
    print('mw',u,kmw,mw_preverb0,mw_preverb)
   rec.mwpreverbs.append(mw_preverb)
   if mw_preverb in mwpreverbs_dict:
    mwprerec = mwpreverbs_dict[mw_preverb]
    mwprerec.used = True
    rec.mwpreverbs_found.append(True)
    rec.mwpreverbs_parse.append(mwprerec.parse)
   else:
    rec.mwpreverbs_found.append(False)
    rec.mwpreverbs_parse.append(None)

def skipmw_unused(rec):
 if rec.line.endswith(('+kf','+BU')):
  return True
 if rec.k1 == rec.parse.replace('+',''):
  return True
 return False
def write_mw_unused(mwrecs):
 fileout = 'preverb1_temp_mw_unused.txt'
 n = 0
 with codecs.open(fileout,'w','utf-8') as f:
  for rec in mwrecs:
   if not rec.used:
    out = rec.line
    if skipmw_unused(rec):
     continue
    n = n + 1
    f.write(out+'\n')
 print(n,"records written to",fileout)

def init_knownupas(filein):
 d = {}
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  for line in f:
   line = line.rstrip('\r\n')
   parts = line.split(' ')
   upa = parts[0]
   d[upa] = 0  # count of upasargas used. initially 0
 return d

if __name__=="__main__": 
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx
 filein1 = sys.argv[2] # ccs_verb_filter.txt
 filein2 = sys.argv[3] # cae_upasargas
 fileout = sys.argv[4] # 
 entries = init_entries(filein)
 dhatus = init_ccsverbs(filein1)
 knownupad = init_knownupas(filein2)

 find_entries(dhatus,entries)  # assign entry to each pwg verb record
 find_upasargas(dhatus,knownupad)  # get list of upasargas
 #non_verb_upasargas(entries)  # debug logic
 #join_upasargas(dhatus,mwdict)
 write(fileout,dhatus)
 #write_mw_unused(mwrecs)
