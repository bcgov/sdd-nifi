#!/usr/bin/python3

#--- Produces stats for each field in a CSV file

import sys
import csv
import re
from collections import Counter

def printf(fmt, *varargs):
	s = fmt % varargs

def fprintf(fp, fmt, *varargs):
	fp.write(fmt % varargs)

def main(argv=None):
	dlm_char     = '"'
	csv_names    = []
	fld_lengths  = []
	xtab         = []
	name_prefix  = name_suffix = ''
	data_records = 0
	field_count  = 0

	if (len(sys.argv) > 4):
		sys.exit("\nUsage: csv-stats.py < raw-csv-file <file-prefix> <file-suffix> [quote_chr]\n\n")

	if (len(sys.argv) > 1):
		name_prefix = sys.argv[1] + '.'

	if (len(sys.argv) > 2):
		name_suffix = sys.argv[2] + '.' if sys.argv[2] else ''

	if (len(sys.argv) > 3):
		dlm_char = sys.argv[3][0]

	#--- Get the field names from the header record
	csv_file = csv.reader(sys.stdin, skipinitialspace=True, quotechar=dlm_char)
	csv_list = next(csv_file)
	field_count = 0

	for field in csv_list:
		# Deal with improper/non-quoted header record fields
		# Ignore if the field is the tail end of an expression that has been parsed onto its own line
		if not ((field[0] == "'") and (field[-1] == ')')):
			# Remove the leading part of the expression, leaving only the field name
			if ('.' in field):
				temp = field[field.index('.')+1:]
				field = re.findall(r"\w+",temp)[0]

			csv_names.append(field)
			xtab.append(Counter())
			fld_lengths.append(0)
			field_count += 1

	#--- Scan the records
	for fields in csv_file:
		data_records += 1

		# Compare the number of record fields to the header fields
		if (len(fields) > len(xtab)):
			sys.exit("\tERROR: Too many fields in line {0} ({1}, expecting {2})\n\n".format(data_records, len(fields), field_count))

		fnum = 0
		for field in fields:
			flen = len(field)

			if (flen > fld_lengths[fnum]):
				fld_lengths[fnum] = flen

			xtab[fnum][field] += 1
			fnum += 1

	#--- Create frequency tables
	print('Csv fields:' + str(field_count))
	print('Fields encountered: ' + str(len(xtab)) + '\n')
	print('(Frequency table : Max field length)')

	i = 0
	for field in csv_names:
		fname = name_prefix + csv_names[i].lower().strip('". ') + '.' + name_suffix + 'tab'
		print(fname + ' ' + str(fld_lengths[i]))
		try:
			f_tab = open(fname, "w")
		except:
			sys.exit("\n\tERROR - Can't create output file! [{filename}]\n".format(filename=fname))

		keys = xtab[i].keys()
		#keys.sort()
		for key in keys:
			fprintf(f_tab, '"%s" %d\n', key, xtab[i][key])

		f_tab.close
		i += 1
sys.exit(main())
