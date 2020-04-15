echo "remake mwverbs"
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
echo "remake mwverbs1"
python mwverbs1.py mwverbs.txt mwverbs1.txt
echo "remake ccs_verb_filter.txt"
python ccs_verb_filter.py ../ccs.txt  ccs_verb_exclude.txt ccs_verb_filter.txt
echo "remake ccs_verb_filter_map.txt"
python ccs_verb_filter_map.py ccs_verb_filter.txt mwverbs1.txt ccs_verb_filter_map.txt
echo "remake ccs_preverb0"
python preverb0.py ../ccs.txt ccs_verb_filter_map.txt cae_upasargas.txt ccs_preverb0.txt

echo "remake ccs_preverb1.txt"
python preverb1.py slp1 ccs_preverb0.txt ccs_verb_filter_map.txt mwverbs1.txt ccs_preverb1.txt
echo "remake ccs_preverb1_deva.txt"
python preverb1.py deva ccs_preverb0.txt ccs_verb_filter_map.txt mwverbs1.txt ccs_preverb1_deva.txt

