## !/usr/bin/python
## function: produce the file that arranges within 3 paths that satisfy each criteria(ATP, CO2, NADH, NADPH)
## output:The output file name that you want (we recommend the input name to be added ‘_top3’) (format : C#####_C##### ATP(CO2,NADH,NADPH) <top3 paths>)


### Import modules
import sys, re, os
from collections import defaultdict
from optparse import OptionParser

def main(argv):
        optparse_usage = 'make_score_dict.py -i <input_path> -k <KEGG_reaction_list> -atp <KEGG_ATP_reaction_info> -co2 <KEGG_CO2_reaction_info> -nadh <KEGG_NADH_reaction_info> -nadph <KEGG_NADPH_reaction_info> -o <ouput_name> -r <root_dir>'
        parser = OptionParser(usage=optparse_usage)
        parser.add_option("-i", "--inputpath", action="store", type="string",
                dest="input_path", help='The input text file of paths of all compound pairs')
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
        parser.add_option("-r", "--rootDir", action="store", type="string",
                dest="root_dir", help='The root directory. All files are generated here.')
        parser.add_option("-o", "--outputname", action="store", type="string",
                dest ="output_name",help='The output file name that you want')
 
        (options, args) = parser.parse_args()
        output_name= []
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
        if options.output_name:
                output_name.append(options.output_name)
        else:
                print 'Error : please write output file name that you want'
        if len(args) > 0:
                output_name += args
        # Run the function
	make_file(input_path, output_name, kegg_reaction, atp_reaction_info, co2_reaction_info, nadh_reaction_info, nadph_reaction_info, root_dir)

### Define function
def read_file(input_file):
	with open(input_file) as f_in:
		txt = (line.rstrip() for line in f_in)
		txt = list(line for line in txt if line)
	return txt


### Prepare dictionaries
def parse_reaction_name(input_file):
	txt = read_file(input_file)

        dic = defaultdict(str)
        for line in txt:
                line_split = line.split(',')
                edge_from = line_split[1]
                edge_to = line_split[2]
                reaction = line_split[0]
                ecoli_info =  line_split[3]
                compound_pair = (edge_from, edge_to)
                dic[compound_pair] = reaction

        return dic

def parse_score(input_file):
	txt = read_file(input_file)

        dic = defaultdict(int)
        for line in txt:
                line_split = line.split(',')
                edge_from = line_split[1]
                edge_to = line_split[2]
                reaction = line_split[0]
                score_info =  line_split[3]
                con_score = (reaction, edge_from, edge_to)
                dic[con_score] = int(score_info)
        return dic


def make_file(input_path, output_name, kegg_reaction, atp_reaction_info, co2_reaction_info, nadh_reaction_info, nadph_reaction_info, root_dir):
        ### run funtions
        D_reaction_name = parse_reaction_name(kegg_reaction)
        D_atp_score = parse_score(atp_reaction_info)
        D_co2_score = parse_score(co2_reaction_info)
        D_nadh_score = parse_score(nadh_reaction_info)
        D_nadph_score = parse_score(nadph_reaction_info)
	
	nx_txt = read_file(input_path)
	output = ''.join(output_name)
	output_file = '%s/%s' % (root_dir, output)
	output_handle = open(output_file, 'w')

	i = 1
	for line in nx_txt:
		if i % 50000 == 0: print i
		i += 1
		line_split = line.split('\t')
		if len(line_split) == 1: continue 
		pair, paths = line_split
		paths_split = paths.split('@')

		D_scores = {}
		for path_element in paths_split:

			done_reactin = []
			compound_list = path_element.split(', ')
			
			atp_score = 0
			co2_score = 0
			nadh_score = 0
			nadph_score = 0
			for comp_from, comp_to in zip(compound_list[0:-1], compound_list[1:]):
				if D_reaction_name[(comp_from, comp_to)]:
					reaction_id = D_reaction_name[comp_from, comp_to]
				else:
					reaction_id = D_reaction_name[comp_to, comp_from]
				if (reaction_id, comp_from, comp_to) in D_atp_score.keys():
					atp_score += D_atp_score[(reaction_id, comp_from, comp_to)]
				elif (reaction_id, comp_to, comp_from) in D_atp_score.keys():
					atp_score += -D_atp_score[(reaction_id, comp_to, comp_from)]
				else:
					atp_score += 0
				if (reaction_id, comp_from, comp_to) in D_co2_score.keys():
                                        co2_score += D_co2_score[(reaction_id, comp_from, comp_to)]
                                elif (reaction_id, comp_to, comp_from) in D_co2_score.keys():
                                        co2_score += -D_co2_score[(reaction_id, comp_to, comp_from)]
                                else:
                                        co2_score += 0
				if (reaction_id, comp_from, comp_to) in D_nadh_score.keys():
                                        nadh_score += D_nadh_score[(reaction_id, comp_from, comp_to)]
                                elif (reaction_id, comp_to, comp_from) in D_nadh_score.keys():
                                        nadh_score += -D_nadh_score[(reaction_id, comp_to, comp_from)]
                                else:
                                        nadh_score += 0
				if (reaction_id, comp_from, comp_to) in D_nadph_score.keys():
                                        nadph_score += D_nadph_score[(reaction_id, comp_from, comp_to)]
                                elif (reaction_id, comp_to, comp_from) in D_nadph_score.keys():
                                        nadph_score += -D_nadph_score[(reaction_id, comp_to, comp_from)]
                                else:
                                        nadph_score += 0

			D_scores[path_element] = (atp_score, co2_score, nadh_score, nadph_score)

		atp_sorted = sorted(D_scores.items(), key=lambda x: x[1][0], reverse=True)
		co2_sorted = sorted(D_scores.items(), key=lambda x: x[1][1], reverse=False)
		nadh_sorted = sorted(D_scores.items(), key=lambda x: x[1][2], reverse=True)
		nadph_sorted = sorted(D_scores.items(), key=lambda x: x[1][3], reverse=True)

		atp_top3 = [x[0] for x in atp_sorted[0:3]]
		co2_top3 = [x[0] for x in co2_sorted[0:3]]
		nadh_top3 = [x[0] for x in nadh_sorted[0:3]]
		nadph_top3 = [x[0] for x in nadph_sorted[0:3]]

		output_handle.write('%s\t%s\t%s\n' % (pair, 'ATP', '@'.join(atp_top3)))
		output_handle.write('%s\t%s\t%s\n' % (pair, 'CO2', '@'.join(co2_top3)))
		output_handle.write('%s\t%s\t%s\n' % (pair, 'NADH', '@'.join(nadh_top3)))
		output_handle.write('%s\t%s\t%s\n' % (pair, 'NADPH', '@'.join(nadph_top3)))
	output_handle.close()

if __name__ == "__main__":
        main(sys.argv[1:])
