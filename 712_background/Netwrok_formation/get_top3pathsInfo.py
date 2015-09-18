## !/usr/bin/python
## function: produce tsv files corresponding to each compound pair and mySQLdb.txt after adding ATP, CO2, NADH, NADPH, equation data about selected top3 paths.
## output: 1) tsv files (C#####_C#####.tsv) 2) mySQLdb.txt (that will be created in <root_dir>)


## import modules
import itertools
import networkx as nx
import json
import urllib2, sys, re, getopt, os, glob, random
import shlex, subprocess
from optparse import OptionParser
from collections import defaultdict
from time import strftime
 
def main(argv):
        optparse_usage = 'get_top3pathsInfo.py -i <input_path> -k <KEGG_reaction_list> -a <KEGG_ATP_reaction_info> -c <KEGG_CO2_reaction_info> -d <KEGG_NADH_reaction_info> -p <KEGG_NADPH_reaction_info> -e <KEGG_equation_info> -r <root_dir>'
        parser = OptionParser(usage=optparse_usage)
        parser.add_option("-i", "--inputpath", action="store", type="string",
                dest="input_path", help='The input text file of top3 paths of all compound pairs')
	parser.add_option("-k", "--keggReaction", action="store", type="string",
                dest="kegg_reaction", help='The input text file including KEGG reaction IDs, compound ID pairs, and E. coli K-12 gene information')
        parser.add_option("-a", "--atpReactionInfo", action="store", type="string",
                dest="atp_reaction_info", help='The input text file including KEGG ATP reaction IDs, compound ID pairs, and ATP change information')
        parser.add_option("-c", "--co2gReactionInfo", action="store", type="string",
                dest="co2_reaction_info", help='The input text file including KEGG CO2 reaction IDs, compound ID pairs, and CO2 change information')
        parser.add_option("-d", "--nadhReactionInfo", action="store", type="string",
                dest="nadh_reaction_info", help='The input text file including KEGG NADH reaction IDs, compound ID pairs, and NADH change information')
        parser.add_option("-p", "--nadphReactionInfo", action="store", type="string",
                dest="nadph_reaction_info", help='The input text file including KEGG NADPH reaction IDs, compound ID pairs, and NADPH change information')
	parser.add_option("-e", "--equationInfo", action="store", type="string",
                dest="equation_info", help='The input text file including KEGG reaction IDs, compound ID pairs, and equation information')
        parser.add_option("-r", "--rootDir", action="store", type="string",
                dest="root_dir", help='The root directory. All files are generated here.')

        (options, args) = parser.parse_args()
        if options.root_dir:
                root_dir = os.path.abspath(options.root_dir)
        else:
                print 'ERROR: please provide proper root direcotory'
        if options.input_path:
                input_path = os.path.abspath(options.input_path)
        else:
                print 'Error: please provide proper input file name'
	if options.kegg_reaction:
                kegg_reaction = os.path.abspath(options.kegg_reaction)
        else:
                print 'Error: please provide proper KEGG reaction file name'
        if options.atp_reaction_info:
                atp_reaction_info = os.path.abspath(options.atp_reaction_info)
        else:
                print 'Error: please provide proper KEGG ATP reaction file name'
        if options.co2_reaction_info:
                co2_reaction_info = os.path.abspath(options.co2_reaction_info)
        else:
                print 'Error: please provide proper KEGG CO2 reaction file name'
        if options.nadh_reaction_info:
                nadh_reaction_info = os.path.abspath(options.nadh_reaction_info)
        else:   
                print 'Error: please provide proper KEGG NADH reaction file name'
        if options.nadph_reaction_info:
                nadph_reaction_info = os.path.abspath(options.nadph_reaction_info)
        else:
                print 'Error: please provide proper KEGG NADPH reaction file name'
	if options.equation_info:
                equation_info = os.path.abspath(options.equation_info)
        else:
                print 'Error: please provide proper equation file name of KEGG reactions'
	
	#Run functions
	print 'START time:\t%s' % (strftime("%Y-%m-%d %H:%M:%S"))
	make_file(input_path, kegg_reaction, atp_reaction_info, co2_reaction_info, nadh_reaction_info, nadph_reaction_info, equation_info, root_dir)
	print 'END time:\t%s' % (strftime("%Y-%m-%d %H:%M:%S"))	

### Define functions
def read_file(input_file):
        with open(input_file) as f_in:
                txt = (line.rstrip() for line in f_in)
                txt = list(line for line in txt if line)
        return txt

#Parse reactions IDs using pairs of compounds
def parse_reaction_name(pathway_link):
        with open(pathway_link) as f_in:
          txt = (line.rstrip() for line in f_in)
          txt = list(line for line in txt if line)
 
        edge_list = []
        dic = defaultdict(str)
        dic2 = defaultdict(str)
        for line in txt:
                line_split = line.split(',')
                edge_from = line_split[1]
                edge_to = line_split[2]
                reaction = line_split[0]
                ecoli_info =  line_split[3]
                edge_list.append((edge_from, edge_to))
                compound_pair = (edge_from, edge_to)
                dic[compound_pair] = (reaction)
                dic2[reaction] = (ecoli_info)
        return dic, dic2, edge_list
 
#Parse Score database using Reaction IDs and pairs of compounds
def parse_score_data(pathway_link):
        with open(pathway_link) as f_in:
          txt = (line.rstrip() for line in f_in)
          txt = list(line for line in txt if line)
 
        dic = defaultdict(str)
        for line in txt:
                line_split = line.split(',')
                edge_from = line_split[1]
                edge_to = line_split[2]
                reaction = line_split[0]
                score_info =  line_split[3]
                con_score = (reaction, edge_from, edge_to)
                dic[con_score] = (score_info)
        return dic
 
# Parse equation database using Reaction IDs 
def parse_equat_data(pathway_link):
        with open(pathway_link) as f_in:
          txt = (line.rstrip() for line in f_in)
          txt = list(line for line in txt if line)
 
        dic_reac = defaultdict(str)
        dic_prod = defaultdict(str)
        for line in txt:
                line_split = line.split('@')
                edge_from = line_split[1].strip()
                edge_to = line_split[2].strip()
                reaction = line_split[0].strip()
                reactants =  line_split[3].strip()
                products = line_split[4].strip()
                compound_pair = (edge_from, edge_to)
                dic_reac[(reaction,edge_from,edge_to)] = reactants
                dic_prod[(reaction,edge_from,edge_to)] = products
        return dic_reac, dic_prod

#obtain the reaction name and direction
def equat_info_in_path(top3paths, Dict_reactions, dic_reac, dic_prod):
        dic_Reaction = defaultdict(list)
        dic_path_com = defaultdict(list)
        dic_path_equat = defaultdict(list)
        j = 1
        k = 0
        while k < len(top3paths):
                done_reaction = []
                done_equat = []
                Reaction = []
                i = 0
                path_name = '%s' % (j)
                while i < len(top3paths[k].split(', ')) - 1:
			top3path = top3paths[k].split(', ')
                        reaction = top3path[i:i+2]
                        (from_comp, to_comp) = reaction
                        if Dict_reactions[(from_comp, to_comp)]:
                                reaction_id = Dict_reactions[(from_comp, to_comp)]
                                Reaction.append(reaction_id)
                                reactants = dic_reac[(reaction_id,from_comp,to_comp)]
                                products = dic_prod[(reaction_id,from_comp,to_comp)]
                                act_G = reaction_id, from_comp, to_comp
                                done_reaction.append(act_G)
                                act_net = reaction_id, reactants, products
                                done_equat.append(act_net)
 
                        else:
                                reaction_id = Dict_reactions[(to_comp, from_comp)]
                                Reaction.append(reaction_id)
                                reactants = dic_reac[(reaction_id,to_comp,from_comp)]
                                products = dic_prod[(reaction_id,to_comp,from_comp)]
                                act_G = reaction_id, from_comp, to_comp
                                done_reaction.append(act_G)
                                act_net = reaction_id, products, reactants
                                done_equat.append(act_net)
                        i += 1
                dic_Reaction[int(path_name)] = Reaction
                dic_path_com[int(path_name)] = done_reaction
                dic_path_equat[int(path_name)] = done_equat
                j += 1
                k += 1
        return dic_Reaction, dic_path_com, dic_path_equat


# calculate the number of score changes in the pathway 
def cal_score(dict_path_com, dict_score):
        D_score = defaultdict(list)
        D_mid = defaultdict(str)
        for key in dict_path_com.keys():
                D_small = {}
                score_change = 0
                for path_element in dict_path_com[key]:
                        reaction_id, from_comp, to_comp = path_element
                        if (reaction_id, from_comp, to_comp) in dict_score.keys():
                                score_num = int(dict_score[path_element])
                                score_change += int(dict_score[path_element])
                        elif (reaction_id, to_comp, from_comp) in dict_score.keys():
				score_num = -int(dict_score[(reaction_id, to_comp, from_comp)])
                                score_change += -int(dict_score[(reaction_id, to_comp, from_comp)])
                        else:        
				score_num = 0
                                score_change += 0
                        D_small[path_element] = score_num
                D_score[key].append(D_small)
                D_mid[key] = score_change
        D_score['final'].append(D_mid)
        return D_score

#get the score information in each pathway
def get_score_info(D_ATP,D_CO2,D_NADH,D_NADPH):
        path1 = []
        path2 = []
        path3 = []
        dic_path = defaultdict(list)
        for value in D_ATP['final']:
                for path in value.keys():
                        if path == 1:
                                path1.append(int(value[path]))
                        elif path == 2:
                                path2.append(int(value[path]))
                        elif path == 3:
                                path3.append(int(value[path]))
        for value in D_CO2['final']:
                for path in value.keys():
                        if path == 1:
                                path1.append(int(value[path]))
                        elif path == 2:
                                path2.append(int(value[path]))
                        elif path == 3:
                                path3.append(int(value[path]))
        for value in D_NADH['final']:
                for path in value.keys():
                        if path == 1:
                                path1.append(int(value[path]))
                        elif path == 2:
                                path2.append(int(value[path]))
                        elif path == 3:
                                path3.append(int(value[path]))
        for value in D_NADPH['final']:
                for path in value.keys():
                        if path == 1:
                                path1.append(int(value[path]))
                        elif path == 2:
                                path2.append(int(value[path]))
                        elif path == 3:
                                path3.append(int(value[path]))
        dic_path[1] = path1
        dic_path[2] = path2
        dic_path[3] = path3
        return dic_path

def get_equat(dic_path_equat):
        dic_final = defaultdict(str)
        for path_name in dic_path_equat.keys():
                reactant = []
                product = []
                Reactant = []
                Product = []
                dic_number_reac = {}
                dic_number_prod = {}
                dic_numberR = {}
                dic_numberP = {}
                for path_info in dic_path_equat[path_name]:
                        for p in path_info[1].split('+'):
                                if re.search(r'^\d+\s.+',p.strip()):
                                        a = re.search(r'^\d+\s(.+)',p.strip()).group(1)
                                        b = re.search(r'^(\d+)\s',p.strip()).group(1)
                                        if a in dic_number_reac.keys():
                                                dic_number_reac[a] += int(b)
                                        else:
                                                dic_number_reac[a] = int(b)
                                else:
                                        if p.strip() in dic_number_reac.keys():
                                                dic_number_reac[p.strip()] += 1
                                        else:
                                                dic_number_reac[p.strip()] = 1
 
                        for q in path_info[2].split('+'):
                                if re.search(r'^\d+\s.+',q.strip()):
                                        a = re.search(r'^\d+\s(.+)',q.strip()).group(1)
                                        b = re.search(r'^(\d+)\s',q.strip()).group(1)
                                        if a in dic_number_prod.keys():
                                                dic_number_prod[a] += int(b)
                                        else:
                                                dic_number_prod[a] = int(b)
                                else:
                                        if q.strip() in dic_number_prod.keys():
                                                dic_number_prod[q.strip()] += 1
                                        else:
                                                dic_number_prod[q.strip()] = 1
                for reac_compound in dic_number_reac.keys():
                        if reac_compound in dic_number_prod.keys():
                                dic_numberR[reac_compound] = dic_number_reac[reac_compound]-dic_number_prod[reac_compound]
                        else:
                                dic_numberR[reac_compound] = dic_number_reac[reac_compound]
                for prod_compound in dic_number_prod.keys():
                        if prod_compound in dic_number_reac.keys():
                                dic_numberP[prod_compound] = dic_number_prod[prod_compound]-dic_number_reac[prod_compound]
                        else:
                                dic_numberP[prod_compound] = dic_number_prod[prod_compound]
                for compound in dic_numberR.keys():
                        if dic_numberR[compound] == 1 :
                                reactant.append('%s' %(compound))
                        elif dic_numberR[compound] > 1 :
                                reactant.append('%s %s' %(dic_numberR[compound],compound))
                for compound in dic_numberP.keys():
                        if dic_numberP[compound] == 1 :
                                product.append('%s' %(compound))
                        elif dic_numberP[compound] > 1:
                                product.append('%s %s' %(dic_numberP[compound],compound))
                a = ' + '.join(reactant)
                b = ' + '.join(product)
                final =  '%s -> %s' %(a,b)
                dic_final[path_name] = final
        return dic_final


def make_file(file_path, kegg_reaction, atp_reaction_info, co2_reaction_info, nadh_reaction_info, nadph_reaction_info, equation_info, root_dir):
        output_file_1 = "mySQLdb.txt" 
 
        output_1 = open(output_file_1,'w')
        output_1.write('C#_C#_path#\tshowname\tATP\tCO2\tNADH\tNADPH\tnet_name\tReactions#\n')

        top3 = read_file(file_path)
        Dict_reactions, Dict_ecoli, edge_list_kegg = parse_reaction_name(kegg_reaction)
        Dict_ATP = parse_score_data(atp_reaction_info)
        Dict_CO2 = parse_score_data(co2_reaction_info)
        Dict_NADH = parse_score_data(nadh_reaction_info)
        Dict_NADPH = parse_score_data(nadph_reaction_info)
        Dict_reac_name, Dict_prod_name = parse_equat_data(equation_info)
	Compoundpair = []
	Compound_pair = []
	i = 1
	first_split = top3[0].split('\t')
	compound_pair, kind, paths = first_split 
	Compound_pair.append(compound_pair)
	output_2 = open('%s.tsv' %(compound_pair),'w')
	output_2.write('id\tshowname\treaction\tchange\n')
        for line in top3:
                if i % 50000 == 0:
                         print '%i lines have been completed' % i
		i += 1
                line_split = line.split('\t')
                compound_pair, kind, paths = line_split 
                paths_split = paths.split('@')
                Dict_path_react, Dict_path_comp, Dict_path_equat_name= equat_info_in_path(paths_split, Dict_reactions, Dict_reac_name, Dict_prod_name)
                D_ATP = cal_score(Dict_path_comp, Dict_ATP)
                D_CO2 = cal_score(Dict_path_comp, Dict_CO2)
                D_NADH = cal_score(Dict_path_comp, Dict_NADH)
                D_NADPH = cal_score(Dict_path_comp, Dict_NADPH)
                Dict_path = get_score_info(D_ATP,D_CO2,D_NADH,D_NADPH)
                Dict_final_name = get_equat(Dict_path_equat_name)
		if not compound_pair in Compound_pair:
			output_2.close()
			output_2 = open('%s.tsv' %(compound_pair),'w')
			output_2.write('id\tshowname\treaction\tchange\n')
		Compoundpair.append(compound_pair)
                Compound_pair = list(set(Compoundpair))
                for path_name in Dict_path_comp.keys():
                        output_1.write('%s_%s_%s\t' % (compound_pair, kind, path_name))
			if kind =="CO2":
				if path_name == 1:	
					output_1.write('1st smallest CO2 loss\t')
				elif path_name == 2:
					output_1.write('2nd smallest CO2 loss\t')
				elif path_name == 3:
					output_1.write('3rd smallest CO2 loss\t')
			elif kind == "ATP":
				if path_name == 1:
                                        output_1.write('1st largest ATP production\t')
                                elif path_name == 2:
                                        output_1.write('2nd largest ATP production\t')
                                elif path_name == 3:
                                        output_1.write('3rd largest ATP production\t')
			elif kind == "NADH":
                                if path_name == 1:
                                        output_1.write('1st largest NADH production\t')
                                elif path_name == 2:
                                        output_1.write('2nd largest NADH production\t')
                                elif path_name == 3:
                                        output_1.write('3rd largest NADH production\t')
			elif kind == "NADPH":
                                if path_name == 1:
                                        output_1.write('1st largest NADPH production\t')
                                elif path_name == 2:
                                        output_1.write('2nd largest NADPH production\t')
                                elif path_name == 3:
                                        output_1.write('3rd largest NADPH production\t') 
                        z = 0
                        while z < len(Dict_path[path_name]):
                                output_1.write('%s\t' % (Dict_path[path_name][z]))
                                z += 1
                        output_1.write('%s\t' % (Dict_final_name[path_name]))
                        output_1.write('%s\n' % (Dict_path_react[path_name]))
                        q = 0
                        w = 1 
			if kind == "ATP":
                                atp_info = D_ATP[path_name]
                                order = Dict_path_comp[path_name]
                                while q < len(order):
                                        output_2.write('%s\t' % (w))
					if path_name == 1:
                                        	output_2.write('1st largest ATP production\t')
                                	elif path_name == 2:
                                        	output_2.write('2nd largest ATP production\t')
                                	elif path_name == 3:
                                        	output_2.write('3rd largest ATP production\t')
                                        output_2.write('%s\t%s\n' % (order[q][0], atp_info[0][order[q]]))
                                        q += 1
                                        w += 1
                        elif kind == "CO2":
                                co2_info = D_CO2[path_name]
                                order = Dict_path_comp[path_name]
                                while q < len(order):
                                        output_2.write('%s\t' % (w))
					if path_name == 1:
                                        	output_2.write('1st smallest CO2 loss\t')
                                	elif path_name == 2:
                                        	output_2.write('2nd smallest CO2 loss\t')
                                	elif path_name == 3:
                                        	output_2.write('3rd smallest CO2 loss\t')
                                        output_2.write('%s\t%s\n' % (order[q][0], co2_info[0][order[q]]))
                                        q += 1
                                        w += 1
                        elif kind == "NADH":
                                nadh_info = D_NADH[path_name]
                                order = Dict_path_comp[path_name]
                                while q < len(order):
                                        output_2.write('%s\t' % (w))
					if path_name == 1:
                                        	output_2.write('1st largest NADH production\t')
                                	elif path_name == 2:
                                        	output_2.write('2nd largest NADH production\t')
                                	elif path_name == 3:
                                        	output_2.write('3rd largest NADH production\t')
                                        output_2.write('%s\t%s\n' % (order[q][0],nadh_info[0][order[q]]))
                                        q += 1
                                        w += 1
                        elif kind == "NADPH":
                                nadph_info = D_NADPH[path_name]
                                order = Dict_path_comp[path_name]
                                while q < len(order):
                                        output_2.write('%s\t' % (w))
					if path_name == 1:
                                        	output_2.write('1st largest NADPH production\t')
                                	elif path_name == 2:
                                        	output_2.write('2nd largest NADPH production\t')
                                	elif path_name == 3:
                                        	output_2.write('3rd largest NADPH production\t')
                                        output_2.write('%s\t%s\n' % (order[q][0], nadph_info[0][order[q]]))
                                        q += 1
                                        w += 1
 
        output_1.close()
	
 
 


if __name__ == "__main__":
        main(sys.argv[1:])
