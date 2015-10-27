#!/usr/bin/python3
import argparse
import csv
import io
import sys
from datetime import datetime

# Script to convert Natasha's Cherokee syllabary table into the format
# used by ibus-table, by Thomas Klute <thomas2.klute@uni-dortmund.de>.
#
# Licensed as CC0 (see
# https://creativecommons.org/publicdomain/zero/1.0/), use as you
# wish!
#
# Usage: ./csv-to-ibus.py [--icon ICON] < chr.csv > chr.txt

parser = argparse.ArgumentParser()
# Use this icon. If not set, a default question mark icon is used.
parser.add_argument("-i", "--icon",
                    help='Icon for the input method, default: py-mode.svg',
                    default='py-mode.svg')
args = parser.parse_args()

# variables for table metadata that's likely to change
desc = "Input method for Cherokee, based on Natasha's syllabary table"
author = "Thomas Klute <thomas2.klute@uni-dortmund.de>"
uuid = "fa824c40-b615-46b0-807d-b9fa311c3a1c"
# simple time based serial number, UTC to avoid any timezone confusion
serial = datetime.utcnow().strftime('%Y%m%d%H%M')



# CSV reader object to parse the syllabary table row by row
reader = csv.DictReader(sys.stdin)
# "buf" is a buffer for the replacement table. Collecting metadata
# (maximum lenght of transliterations, valid characters) requires
# parsing the input before writing the file header.
buf = io.StringIO()
# used to remember the maximum length of transliterations
maxlen = 0
# set to collect all characters occurring in transliterations
valid_chars = set()

# Dictionary with transliterations (keys) and character combinations
# (values) for nah* quirks. Input sequences for "na-h*" character
# combinations overlap with the "nah" character. This dictionary
# contains combined replacements for such combinations so the user
# can choose easily.
nah_quirks = dict()

# Create the replacement table. All replacements are assigned the same
# frequency since there's only one replacement per combination of
# input characters.
for row in reader:
    # line format (TSV): transliteration, character, frequency
    print("%s\t%s\t%d" % (row['transliteration'], row['character'], 1),
          file=buf)
    if len(row['transliteration']) > maxlen:
        maxlen = len(row['transliteration'])
    valid_chars |= set(row['transliteration'])
    # process transliterations starting with 'h' for nah* quirks
    if row['transliteration'][0] == 'h' and len(row['transliteration']) > 1:
        k = 'na' + row['transliteration']
        nah_quirks[k] = '\u13be' + row['character']
        if len(k) > maxlen:
            maxlen = len(k)



# file type header
print("SCIM_Generic_Table_Phrase_Library_TEXT\n"
      "VERSION_1_0\n")

# table metadata
print("BEGIN_DEFINITION\n"
      "LICENSE = CC0\n"
      "SYMBOL = \u13e3\n"
      "NAME = Cherokee\n"
      "LANGUAGES = chr\n"
      "STATUS_PROMPT = \u13e3\u13b3\u13a9")

# Just one replacement per print() to avoid mixups
print("UUID = %s" % uuid)
print("SERIAL_NUMBER = %s" % serial)
print("ICON = %s" % args.icon)
print("DESCRIPTION = %s" % desc)
print("AUTHOR = %s" % author)
print("VALID_INPUT_CHARS = %s" % str().join(sorted(valid_chars)))
print("MAX_KEY_LENGTH = %d" % maxlen)

# This is a static replacement table, so use autocommit (just type, no
# need to confirm replacements), and no complicated stuff.
print("LAYOUT = default\n"
      "AUTO_COMMIT = TRUE\n"
      "AUTO_SELECT = TRUE\n"
      "DEF_FULL_WIDTH_PUNCT = FALSE\n"
      "DEF_FULL_WIDTH_LETTER = FALSE\n"
      "USER_CAN_DEFINE_PHRASE = FALSE\n"
      "PINYIN_MODE = FALSE\n"
      "DYNAMIC_ADJUST = FALSE\n"
      "END_DEFINITION\n")

print('BEGIN_TABLE')

# Write buffered table to output
sys.stdout.write(buf.getvalue())

# Add quirks for sequences starting with nah
for k in nah_quirks.keys():
    print("%s\t%s\t%d" % (k, nah_quirks[k], 1))

print('END_TABLE')
