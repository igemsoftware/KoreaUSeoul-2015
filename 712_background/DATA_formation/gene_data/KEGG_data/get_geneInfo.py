#!/usr/bin/python

'''
Download enzyme database
Column - E.C. number, Gene list
'''


### Import modules
from httplib import *
import re, sys, os, glob
from optparse import OptionParser


### Parameters
output_dir = '/home/shkim/iGEM/GeneGene'


def main(argv):
        optparse_usage = 'get_geneInfo.py -i <kegg_reaction> -r <root_dir>'
        parser = OptionParser(usage=optparse_usage)
        parser.add_option("-i", "--kegg_reaction", action="store", type="string",
                dest="kegg_reaction", help='kegg_reaction_ec.tsv')
        parser.add_option("-r", "--rootDir", action="store", type="string",
                dest="root_dir", help='The root directory. All files will be generated here.')

        (options, args) = parser.parse_args()
        if options.root_dir:
                root_dir = os.path.abspath(options.root_dir)
        else:
                print 'ERROR: please provide proper root direcotory'

        if options.kegg_reaction:
                kegg_reaction = os.path.abspath(options.kegg_reaction)
        else:
                print 'ERROR: please provide proper kegg_reaction_ec.tsv'

# Run the function
        create_dir(root_dir)
        reaction_txt = read_file(kegg_reaction)
        num = 1
        for line in reaction_txt[0:]:
                line_split = line.split('\t')
                reaction_id = line_split[0]
                enzyme = line_split[1]

                # Download and write to file
                output_faa_file = os.path.join(output_dir, '%s' % (reaction_id))
                output_handle = open(output_faa_file, 'w')

                idx = enzyme.find('///')
                while (idx > 0):
                        en1 = enzyme[:idx]

                        write_txt(output_handle, en1)


                        enzyme = enzyme[idx+3:]
                        idx = enzyme.find('///')

                en1 = enzyme.rstrip()
                if (en1 != ''):
                        write_txt(output_handle, en1)

                output_handle.close()


def create_dir(root_dir):
        output_dir = os.path.join(root_dir, 'GeneGene')
        if not glob.glob(output_dir):
                command = 'mkdir %s' % (output_dir)
                os.system(command)


def read_file(input_file):
        with open(input_file) as f_in:
                txt = (line for line in f_in)
                txt = list(line for line in txt if line)
        return txt


def write_txt(output_handle, en1):
        output_handle.write(en1)
        output_handle.write('\n')
        output_handle.write('##########\n')

        if en1 == '':
                return

        idx = en1.find('-')
        if idx < 1:
                fname = 'ec:' + en1 + '.faa'
                fname = 'Enzyme/' + fname
                print '... reading ', fname
                temp = read_file(fname)

                for line in temp[0:]:
                        output_handle.write(line)

if __name__ == "__main__":
    main(sys.argv[1:])
