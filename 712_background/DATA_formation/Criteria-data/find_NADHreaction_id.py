## !/usr/bin/python
## function:
## input:
## output:

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


## what is your goal(G)?
G = 'C000
goal = 'NADH'



### get the reactions concerning NADH and save it
 
NADH_rn_file = 'http://rest.kegg.jp/link/reaction/C00004'
NADH_rn = download_file(NADH_rn_file)

output_file = 'NADH_reaction_id.txt'
output = open(output_file,'w')

for line in NADH_rn:
	if re.search(r'rn:(R\d+)',line):
		rn = re.findall(r'rn:(R\d+)',line)
		Rn = ''.join(rn)
		output.write('%s\n' % (Rn))
output.close()
