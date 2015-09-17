## !/usr/bin/python
## function: save the KEGG reaction list related to CO2.
## output:'CO2_reaction_id.txt'

## import modules

import itertools
import networkx as nx
import json
import urllib2, sys, re
from collections import defaultdict
 
## define the function#1 to download the information

def download_file(path):
	data = urllib2.urlopen(path, timeout = 200).read()
	data_split = data.split('\n')

	return data_split

### get the reactions concerning CO2 and save it
 
CO2_rn_file = 'http://rest.kegg.jp/link/reaction/C00011'
CO2_rn = download_file(CO2_rn_file)

output_file = 'CO2_reaction_id.txt'
output = open(output_file ,'w')

for line in CO2_rn:
	if re.search(r'rn:(R\d+)',line):
		rn = re.findall(r'rn:(R\d+)',line)
		Rn = ''.join(rn)
		output.write('%s\n' % (Rn))
output.close()
