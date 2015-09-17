## !/usr/bin/python
## function: save the KEGG reaction list related to ATP.
## output: : 'ATP_reaction_id.txt'

## import modules
import itertools
import networkx as nx
import json
import urllib2, sys, re
from collections import defaultdict
 
## define the function to download the information

def download_file(path):
	data = urllib2.urlopen(path, timeout = 200).read()
	data_split = data.split('\n')

	return data_split


### get the reactions concerning ATP and ADP and save it
 
ATP_rn_file = 'http://rest.kegg.jp/link/reaction/C00002'
ATP_rn = download_file(ATP_rn_file)

output_file = 'ATP_reaction_id.txt'
output = open(output_file ,'w')
 
for line in ATP_rn:
        if re.search(r'rn:(R\d+)',line):
                rn = re.findall(r'rn:(R\d+)',line)
                Rn = ''.join(rn)
                output.write('%s\n' % (Rn))
output.close() 
