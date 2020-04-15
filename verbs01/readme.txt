
Analysis of ccs verbs and upasargas, revised
This work was done in a temporary subdirectory (temp_verbs) of csl-orig/v02/ccs/.

The shell script redo.sh reruns  python programs, from mwverb.py to preverb1.py.


* mwverbs
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
#copy from v02/mw/temp_verbs
#cp ../../mw/temp_verbs/verb.txt mwverbs.txt
each line has 5 fields, colon delimited:
 k1
 L
 verb category: genuinroot, root, pre,gati,nom
 cps:  classes and/or padas. comma-separated string
 parse:  for pre and gati,  shows x+y+z  parsing prefixes and root

* mwverbs1.txt
python mwverbs1.py mwverbs.txt mwverbs1.txt
Merge records with same key (headword)
Also  use 'verb' for categories root, genuineroot, nom
and 'preverb' for categories pre, gati.
Format:
 5 fields, ':' separated
 1. mw headword
 2. MW Lnums, '&' separated
 3. category (verb or preverb)
 4. class-pada list, ',' separated
 5. parse. Empty for 'verb' category. For preverb category U1+U2+...+root

* ccs_verb_filter.

python ccs_verb_filter.py ../ccs.txt   ccs_verb_exclude.txt ccs_verb_filter.txt

In contrast to CAE, where previous verb identification markup was present,
in CCS verbs must be identified by some other patterns.
The basic pattern is that, within the Devanagari text of an entry, there should
appear a present tense 3rd person singular verb ending 'ti' or 'te'.
The regex used is `u'¦.*t[ie][,) ]*#}'`.  
The first line of the text should also NOT include a pattern indicating
a noun or adverb.  Also, several false-positive entries are excluded,
in the ccs_verb_exclude.txt file.

By this method, 1009 entries are identified as verbs.
By comparison, 1078 entries of the CAE dictionary are identified as verbs.

Format of file ccs_verb_filter.txt:
;; Case 0001: L=191, k1=aNkay, k2=aNkay, code=V
;; Case 0002: L=199, k1=aNKay, k2=aNKay, code=V

* ccs_verb_filter_map
python ccs_verb_filter_map.py ccs_verb_filter.txt mwverbs1.txt ccs_verb_filter_map.txt

Get correspondences between ccs verb spellings and
 - ccs verb spellings
 - mw verb spellings

Format of ccs_verb_filter_map.txt:
 Adds a field mw=xxx to each line of ccs_verb_filter.txt,
indicating the MW root believed to correspond to the CCS root.
For example, aNkay in CCS is believed to correspond to aNk in MW.
;; Case 0001: L=191, k1=aNkay, k2=aNkay, code=V, mw=aNk
;; Case 0002: L=199, k1=aNKay, k2=aNKay, code=V, mw=aNK


In 9 cases, no correspondence could be found. These use 'mw=?'. 
;; Case 0027: L=1964, k1=avataMsay, k2=avataMsay, code=V, mw=?
;; Case 0243: L=7128, k1=culukay, k2=culukay, code=V, mw=?
;; Case 0446: L=11923, k1=nigaqay, k2=nigaqay, code=V, mw=?
;; Case 0464: L=13193, k1=patnIy, k2=patnIy, code=V, mw=?
;; Case 0465: L=13196, k1=paty, k2=paty, code=V, mw=?
;; Case 0567: L=17665, k1=BogAy, k2=BogAy, code=V, mw=?
;; Case 0793: L=22798, k1=virUpay, k2=virUpay, code=V, mw=?
;; Case 0989: L=29379, k1=hAs, k2=hAs, code=V, mw=?
;; Case 0997: L=29655, k1=homay, k2=homay, code=V, mw=?

* ccs_preverb0.txt
python preverb0.py ../ccs.txt ccs_verb_filter_map.txt cae_upasargas.txt ccs_preverb0.txt 

There is no clear identification of upasargas within verb entries of CCS.
Rather, upasargas only appear as Devanagari text.
But there is also much other Devanagari text  (such as different verb forms,
participles, etc.)
So the approach taken to identify upasargas within verb entries makes use
of the list of upasargas that appear within the CAE dictionary.  This
list, in cae_upasargas.txt, contains 142 upasargas (the base upasargas along
with various compound upasargas) that were previously identified as 
occurring within the verb entries of Cappeller's Sanskrit-English dictionary.
In addition, this file contains 8 additional compound upasargas that were
noticed to occur within one or another CCS entry.

Then, for a given verb entry of CCS , all the Devanagari words of the entry
were examined, and those words appearing in the list of compound upasargas
were considered to be the upasargas for that verb entry of CCS.

Further, this computed list of upasargas for each entry was compared with
the underlying text of the CCS entry to confirm the list.  This list 
appears in the ccs_preverb0.txt file

Two typical lines of ccs_preverb0.txt are:
;; Case 0003: L=200, k1=aNg, #upasargas=0, upasargas=
;; Case 0004: L=229, k1=ac, #upasargas=3, upasargas=A,ud,pari

* ccs_preverb1.txt
python preverb1.py slp1 ccs_preverb0.txt ccs_verb_filter_map.txt mwverbs1.txt ccs_preverb1.txt
python preverb1.py deva ccs_preverb0.txt ccs_verb_filter_map.txt mwverbs1.txt ccs_preverb1_deva.txt

For each of the entries of ccs_verb_filter_map.txt, the program uses
the list of upasargas for the entry as it appears in ccs_preverb0.txt.

The number of upasargas found is reported on a line for the verb entry.
The first CCS verb entry has no upasargas:
;; Case 0001: L=191, k1=aNkay, k2=aNkay, code=V, #upasargas=0, mw=aNk (diff)

The fourth CCS verb entry has 3 upasargas:
```
;; Case 0004: L=229, k1=ac, k2=ac, code=V, #upasargas=3 (1/2), mw=ac (same)
01          A         ac                   Ac                   Ac yes A+ac
02         ud         ac                 udac                 udac no 
03       pari         ac               paryac               paryac no 
```
For each upasarga, an attempt is made to match the prefixed verb to a
known MW prefixed verb.  
In this example, one prefixed form was found as in MW verbs (Ac);
while 2 prefixed forms were not found as MW verbs.

Of the 1009 verbs, 525 have no upasargas, and 484 have one or more upasargas.
The total number of upasargas found is 2115.
Of these, 1986 are matched to MW prefixed verbs (match ' yes'),
and 129 are not matched to MW prefixed verbs.



