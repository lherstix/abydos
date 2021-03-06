#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2014-2015 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.

"""features_csv_to_dict.py

This script converts a CSV document of feature values to a Python dict.

The CSV document is of the format
<phonetic symbol(s)>,<variant number>,<segmental>,<feature>+

    Phonetic symbols are IPA (or other system) symbols.
    Variant number refers to one of the following codes:
         0 = IPA
         1 = Americanist
         2 = IPA variant
         3 = Americanist variant
         9 = other
    Segmental must be either 1 (segmental) or 0 (featural). Featural symbols
    replace features on the preceding segmental symbol.
    Features may be 1 (+), -1 (-), or 0 (0) to indicate feature values.

Lines beginning with # are interpreted as comments
"""

from __future__ import unicode_literals, print_function
import sys
import getopt
import codecs
import unicodedata


def main(argv):
    """Main conversion script
    """
    first_col = 3
    last_col = -1

    def print_usage():
        """Print usage statement
        """
        print('features_csv_to_dict.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    def binarize(num):
        """Replace 0, -1, 1, 2 with 00, 10, 01, 11
        """
        if num == '0':      # 0
            return '00'
        elif num == '-1':   # -
            return '10'
        elif num == '1':    # +
            return '01'
        elif num == '2':    # ± (segmental) or copy from base (non-segmental)
            return '11'

    def init_termdicts():
        """Initialize the terms dict
        """
        ifile = codecs.open('features_terms.csv', 'r', 'utf-8')

        feature_mask = dict()
        keyline = ifile.readline().strip().split(',')[first_col:last_col]
        mag = len(keyline)
        for i in range(len(keyline)):
            features = '0b' + ('00' * i) + '11' + ('00' * (mag - i - 1))
            feature_mask[keyline[i]] = int(features, 2)

        termdict = dict()
        for line in ifile:
            line = line.strip().rstrip(',')
            if '#' in line:
                line = line[:line.find('#')].strip()
            if line:
                line = line.split(',')
                term = line[last_col]
                # print line[first_col:last_col]
                features = '0b' + ''.join([binarize(val) for val
                                           in line[first_col:last_col]])
                termdict[term] = int(features, 2)

        return termdict, feature_mask

    def check_terms(sym, features, name, termdict):
        """Check each term of the phone name to confirm that it matches
        the expected features implied by that feature
        """
        if '#' in name:
            name = name[:name.find('#')].strip()
        for term in name.split():
            if term in termdict:
                if termdict[term] & features != termdict[term]:
                    # print termdict[term], features & termdict[term]
                    print('Feature mismatch for term "' + term +
                          '" in   ' + sym)
            else:
                print('Unknown term "' + term + '" in ' + name + ' : ' + sym)

    def check_entailments(sym, features, name, feature_mask):
        """Check for necessary feature assignments (entailments)
        For example, [+round] necessitates [+labial]
        """
        entailments = {'+labial': ('±round', '±protruded', '±compressed',
                                   '±labiodental'),
                       '-labial': ('0round', '0protruded', '0compressed',
                                   '0labiodental'),
                       '+coronal': ('±anterior', '±distributed'),
                       '-coronal': ('0anterior', '0distributed'),
                       '+dorsal': ('±high', '±low', '±front', '±back',
                                   '±tense'),
                       '-dorsal': ('0high', '0low', '0front', '0back',
                                   '0tense'),
                       '+pharyngeal': ('±atr', '±rtr'),
                       '-pharyngeal': ('0atr', '0rtr'),

                       '+protruded': ('+labial', '+round', '-compressed'),
                       '+compressed': ('+labial', '+round', '-protruded'),

                       '+glottalic_suction': ('-velaric_suction',),
                       '+velaric_suction': ('-glottalic_suction',),
                       }

        if '#' in name:
            name = name[:name.find('#')].strip()
        for feature in entailments:
            fname = feature[1:]
            if feature[0] == '+':
                fm = (feature_mask[fname] >> 1) & feature_mask[fname]
            else:
                fm = (feature_mask[fname] << 1) & feature_mask[fname]
            if (features & fm) == fm:
                for ent in entailments[feature]:
                    ename = ent[1:]
                    if ent[0] == '+':
                        efm = (feature_mask[ename] >> 1) & feature_mask[ename]
                    elif ent[0] == '-':
                        efm = (feature_mask[ename] << 1) & feature_mask[ename]
                    elif ent[0] == '0':
                        efm = 0
                    elif ent[0] == '±':
                        efm = feature_mask[ename]

                    if ent[0] == '±':
                        if (features & efm) == 0:
                            print('Incorrect entailment for ' + sym +
                                  ' for feature ' + fname +
                                  ' and entailment ' + ename)
                    else:
                        if (features & efm) != efm:
                            print('Incorrect entailment for ' + sym +
                                  ' for feature ' + fname +
                                  ' and entailment ' + ename)

    checkdict = dict()  # a mapping of symbol to feature
    checkset_s = set()  # a set of the symbols seen
    checkset_f = set()  # a set of the feature values seen

    termdict, feature_mask = init_termdicts()

    ifile = ''
    ofile = ''
    try:
        opts = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])[0]
    except getopt.GetoptError:
        print_usage()
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
        elif opt in ("-i", "--ifile"):
            ifile = codecs.open(arg, 'r', 'utf-8')
        elif opt in ("-o", "--ofile"):
            ofile = codecs.open(arg, 'w', 'utf-8')
    if not ifile:
        print_usage()

    oline = 'PHONETIC_FEATURES = {'
    if not ofile:
        print(oline)
    else:
        ofile.write(oline + '\n')

    keyline = ifile.readline().strip().split(',')[first_col:last_col]
    for line in ifile:
        line = line.strip().rstrip(',')

        if line.startswith('####'):
            break

        line = unicodedata.normalize('NFC', line)

        oline = ''
        if not line or line.startswith('#'):
            oline = '                     '+line

        else:
            line = line.strip().split(',')
            if '#' in line:
                line = line[:line.find('#')]
            symbol = unicode(line[0])
            variant = int(line[1])
            segmental = bool(line[2])
            features = '0b' + ''.join([binarize(val) for val
                                       in line[first_col:last_col]])
            name = line[-1].strip()
            if not segmental:
                features = '-' + features

            featint = int(features, 2)
            check_terms(symbol, featint, name, termdict)
            check_entailments(symbol, featint, name, feature_mask)
            if symbol in checkset_s:
                print('Symbol ' + symbol + ' appears twice in CSV.')
            else:
                checkset_s.add(symbol)

            if variant < 2:
                if featint in checkset_f:
                    print('Feature set ' + unicode(featint) +
                          ' appears in CSV for two primary IPA symbols: ' +
                          symbol + ' and ' + unicode(checkdict[featint]))
                else:
                    checkdict[featint] = symbol
                    checkset_f.add(featint)

            if variant < 5:
                oline = '                     \'{}\': {},'.format(symbol,
                                                                  featint)
            else:
                oline = ''

        if oline:
            if not ofile:
                print(oline)
            else:
                ofile.write(oline + '\n')

    oline = '                    }'
    if not ofile:
        print(oline)
    else:
        ofile.write(oline + '\n')

    oline = '\nFEATURE_MASK = {'
    if not ofile:
        print(oline)
    else:
        ofile.write(oline + '\n')

    mag = len(keyline)
    for i in range(len(keyline)):
        features = int('0b' + ('00' * i) + '11' + ('00' * (mag - i - 1)), 2)
        oline = '                \'{}\': {},'.format(keyline[i], features)
        if not ofile:
            print(oline)
        else:
            ofile.write(oline + '\n')

    oline = '               }'
    if not ofile:
        print(oline)
    else:
        ofile.write(oline + '\n')


if __name__ == "__main__":
    main(sys.argv[1:])
