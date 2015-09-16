## !/usr/bin/python
## function:
## input:
## output:

## import modules
import urllib2, re, sys
from collections import defaultdict

url = 'http://rest.kegg.jp/list/reaction'
data = urllib2.urlopen(url, timeout = 20).read()
data_split = data.split('\n')


output_file = open('all_reaction_id.txt','w')

for line in data_split:
	reaction_id = re.findall(r'rn:(R\d+)', line)
	output_file.write('%s\n' %(''.join(reaction_id)))
	
output_file.close()
