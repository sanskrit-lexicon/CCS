#-*- coding:utf-8 -*-
"""ccs_verb_filter_map.py
"""
from __future__ import print_function
import sys, re,codecs

class Ccsverb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), code=(.*)$',line)
  try:
   self.L,self.k1,self.k2,self.code = m.group(1),m.group(2),m.group(3),m.group(4)
  except:
   print('Ccsverb error:',line)
   exit(1)
  self.pw=None
  self.mw = None
 
def init_ccsverb(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Ccsverb(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

class Pwmw(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.pw,self.mw = line.split(':')
 
def init_pw_mw(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Pwmw(x) for x in f if not x.startswith(';')]
 print(len(recs),"records read from",filein)
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
 #recs = [r for r in recs if r.cat == 'verb']
 print(len(recs),"verbs returned from mwverbs")
 d = {}
 for rec in recs:
  k1 = rec.k1
  if k1 in d:
   print('init_mwverbs: Unexpected duplicate',k1)
  d[k1] = rec
 return recs,d

map2mw_special = {
 'aNkay':'aNk',
 'aNKay':'aNK',
 'ar':'f',
 'arC':'fC',
 'arD':'fD',
 'arz':'fz',
 'kar':'kf', 
 'kart':'kft', 
 'karS':'kfS',
 'kalp':'kxp',
 'kavalay':'kavalaya',
 'gar':'gF',
 'garD':'gfD',
 'Garz':'Gfz',
 'cUrRay':'cUrR',
 'tard':'tfd',
 'tarz':'tfz',
 'dar':'df',
 'darB':'dfB', 
 'darh':'dfh', 
 'DanIy':'DanIya', 
 'Dar':'Df', 
 'Darz':'Dfz', 
 'DUmay':'DUmaya', 
 'DUlay':'DUlaya', 
 'Dvar':'Dvf', 
 'par':'pf', # and/or pF
 'barh':'bfh', 
 'mar':'mf', 
 'marc':'mfc', 
 'marj':'mfj', 
 'marD':'mfD', 
 'mUrcC':'mUrC', 
 'mfgya':'mfg', 
 'yucC':'yuC', 
 'laGay':'laGaya', 
 'liKApay':'liK',  #causal
 'var':'vf', 
 'vart':'vft', 
 'varD':'vfD', 
 'varmay':'varmaya', 
 'varz':'vfz', 
 'vipakzay':'vipakzaya', 
 'vfzasy':'vfzasya', 
 'SvetAy':'SvetAya', 
 'zaRQay':'zaRQaya', 
 'star':'stf', 
 'starh':'stfh', 
 # 'sparD':'spfD', 
 'sparS':'spfS', 
 'smar':'smf', 
 'hvar':'hvf', 
 'hvA':'hve', 
 'tar':'tF',  
 'avaDIray':'avaDIr', # preverb
 'Ips':'Ap', # desid.
 'utkaRW':'utkaRWa',  # 
 'utsukay':'utsukAya',  # 
 'unmUl':'unmUla',  # 
 'Urjay':'Urj',  # 
 'karz':'kfz',  # 
 'kutsay':'kuts',  # 
 'kurukurAy':'KuruKurAya',  # 
 'kzA':'kzE',  # 
 'KaRqay':'KaRq',  # 
 'gUrDay':'gUrD',  # 
 'gfBay':'gfBAya',  # 
 'glA':'glE',  # 
 #'culukay':'culukay',  # 
 'Card':'Cfd',  # 
 'Calay':'Cal',  # 
 'CA':'Co',  # 
 'jar':'jf',  # 
 'waNkay':'waNk',  # 
 'tandrAy':'tandr',  # 
 'taraMg':'taraMga',  # 
 'dIDi':'dI',  # 
 'dyutay':'dyut',  # 
 'drAGay':'drAG',  # 
 #'nigaqay':'nigaqaya',  # 
 'patay':'pat',  # 
 #'patnIy':'patnIy',  # 
 #'paty':'paty',  # 
 'piRqay':'piRq',  # 
 'pUray':'pF',  # 
 'pyA':'pyE',  # 
 'prakASay':'prakAS',  # 
 #'Pakka':'Pakka',  # 
 'bIBats':'bAD',  # 
 #'BogAy':'BogAy',  # 
 'mantray':'mantr',  # 
 'miSray':'miSr',  # 
 'rUkzay':'rUkz',  # 
 'rUpay':'rUp',  # 
 'vanuz':'vanuzya',  # 
 'vasAy':'vas',  # 
 #'virUpay':'virUpay',  # xx
 'vIray':'vIrAya',  # 
 'vfzaRy':'vfzAya',  # ?
 'vyA':'vye',  # 
 'vraRay':'vraR',  # 
 'Sat':'Sad',  # 
 'Sabday':'Sabd',  # 
 'SabdApay':'Sabd',  # 
 'SarD':'SfD',  # 
 'SarD':'SfD',  # 
 'SIlay':'SIl',  # 
 'SuBay':'SuB',  # 
 'SyA':'SyE',  # 
 'Sruz':'Sru',  # 
 'SvA':'Svi',  # 
 'saBAjay':'saBAj',  # 
 'sA':'si',  # 
 'sAntvay':'sAntv',  # 
 'suKay':'suK',  # 
 'sUcay':'sUc',  # 
 'sUtray':'sUtr',  # 
 'stenay':'sten',  # 
 'styA':'styE',  # 
 'sPuway':'sPuw',  # 
 #'hAs':'hAs',  # 
 #'homay':'homay',  # 
 'arTay':'arT',  # 
 #'avataMsay':'avataMsay',  #
 'kaTay':'kaT',  #
 'kIrtay':'kIrt',  #
 'gaRay':'gaR',  #
 #'culukay':'culukay',  #
 'jramB':'jfmB',  #
 'tarp':'tfp',  #
 'trA':'trE',  #
 'darp':'dfp',  #
 'dIdi':'dI',  #
 'DyA':'DyE',  #
 'nart':'nft',  #
 #'patnIy':'patnIy',  #
 #'paty':'paty',  #
 'parc':'pfc',  #
 'pAlay':'pAl',  #
 'Bar':'Bf',  #
 #'BogAy':'BogAy',  #
 'marq':'mfq',  #
 'mard':'mfd',  #
 'marS':'mfS',  #
 'marz':'mfz',  #
 'mfgay':'mfg',  #
 'mokzay':'mokz',  #
 'mlA':'mlE',  #
 'lakzay':'lakz',  #
 'varRay':'varR',  #
 'vAsay':'vas',  #
 'Sar':'SF',  #
 'sar':'sf',  #
 'sarp':'sfp',  #
 'spar':'spf',  #
 'sparh':'spfh',  #
 'har':'hf',  #
 'harz':'hfz',  #
 #'hAs':'hAs',  #
 #'homay':'homay',  #
 'yantray':'yantr',
 'raj':'raYj',
 'svar':'svf',
 'sA':'so',  # also MW 'si'.
 }
map2mw_special_L = {
 '4393':'kF', # k1 = kar
 '26777':'sfj', # k1 = sarj
}

def map2mw(d,k1,L):
 if L in map2mw_special_L:
  k =  map2mw_special_L[L]
  if k in d:
   return k
  else:
   print('map2mw anomaly 1',L,k1,k)
 if k1 in map2mw_special:
  k = map2mw_special[k1]
  if k in d:
   return k
  else:
   print('map2mw anomaly 1',L,k1,k)
 if k1 in d:
  return k1

 if k1.endswith('y'):
  k = k1 + 'a'
  if k in d:
   return k
 
 return '?'


def ccsmap(recs,mwd):
 for rec in recs:
  rec.mw = map2mw(mwd,rec.k1,rec.L)
  #if rec.k1 in ['aNkay','aNKay']:print('ccsmap chk: %s -> %s (%s)' %(rec.k1,rec.mw,rec.mw in mwd))
def write(fileout,recs):
 n = 0
 nomw = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   n = n + 1
   line = rec.line
   # add mw
   out = '%s, mw=%s' %(line,rec.mw)
   if rec.mw == '?':
    nomw = nomw + 1
   f.write(out + '\n')
 print(n,"records written to",fileout)
 print(nomw,"records not yet mapped to mw")


if __name__=="__main__": 
 filein = sys.argv[1] #  ccs_verb_filter.txt
 filein1 = sys.argv[2] # mwverbs1
 fileout = sys.argv[3]

 recs = init_ccsverb(filein)
 mwverbrecs,mwverbsd= init_mwverbs(filein1)
 ccsmap(recs,mwverbsd)
 write(fileout,recs)
