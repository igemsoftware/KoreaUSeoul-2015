import urllib2
import sys, re

database = open('/home/dhkim/table_making/compound_id.txt', 'r')
for names in database:
    mainbody = 'http://www.kegg.jp/dbget-bin/www_bget?'
    tails = names
    adress = '%s%s' % (mainbody, tails)

    f = urllib2.urlopen(adress)

    chemical_name = ''
    formula = ''
    exact_mass = ''
    mol_weight = ''
    i = 1
    k = 0
    for line in f:
        if i == 157:
            line_split = line.split('>')
            chemical_name = '%s%s%s' % ('<td>', line_split[3][:-3], '</td>')
            i += 1
        elif i == 158 and line.rstrip() != '</div></div></td></tr>':
            i += 1
            k += 1
        elif i == 159 and line.rstrip() != '</div></div></td></tr>' and k == 1:
            i += 1
            k += 1
        elif i == 160 and line.rstrip() != '</div></div></td></tr>' and k == 2:
            i += 1
            k += 1
        elif i == 161 and line.rstrip() != '</div></div></td></tr>' and k == 3:
            i += 1
            k += 1
        elif i == 162 and line.rstrip() != '</div></div></td></tr>' and k == 4:
            i += 1
            k += 1
        elif i == 163 and line.rstrip() != '</div></div></td></tr>' and k == 5:
            i += 1
            k += 1
        elif i == 164 and line.rstrip() != '</div></div></td></tr>' and k == 6:
            i += 1
            k += 1
        elif i == 165 and line.rstrip() != '</div></div></td></tr>' and k == 7:
            i += 1
            k += 1
        elif i == 166 and line.rstrip() != '</div></div></td></tr>' and k == 8:
            i += 1
            k += 1
        elif i == 162 + int(k):
            line_split = line.split('>')
            formula = '%s%s%s' % ('<td>', line_split[2][:-3], '</td>')
            i += 1
        elif i == 167 + int(k):
            line_split = line.split('>') 
            if line_split[2] != '<br':
                exact_mass = '%s%s%s' % ('<td>', line_split[2][:-3], '</td>')
                i += 1
            else :
                exact_mass = '%s' % ('<td>No data</td>')
                i += 1
        elif i == 172 + int(k):
            line_split = line.split('>')
            if line_split[2] != '<br':
                mol_weight = '%s%s%s' % ('<td>', line_split[2][:-3], '</td>')
                i += 1
            else :
                mol_weight = '%s' % ('<td>No data</td>')
                i += 1
        else:
            i += 1

    table_format = open('/home/dhkim/table_making/table_format.txt', 'r')
    final = ''
    n1 = '<td class="tg-x0js"> <image src="http://www.genome.jp/Fig/compound/'
    n2 = '.gif" width="150" height="100" ></td>'
    img = '%s%s%s' % (n1, tails.rstrip(), n2)
    j = 1
    for sets in table_format:
        if j == 6:
            final += '%s%s%s' % ('<caption>', tails.rstrip(), '</caption>')
            j += 1
        elif j == 9:
            final += chemical_name
            j += 1
        elif j == 13:
            final += formula
            j += 1
        elif j == 17:
            final += exact_mass
            j += 1
        elif j == 21:
            final += mol_weight
            j += 1
        elif j == 25:
            final += img
            j += 1
        else:
            final += sets
            j += 1
    ff = '%s.html' % (tails.rstrip())
    output = open(ff, 'w')
    output.write('%s' % (final)) 
    output.close()
