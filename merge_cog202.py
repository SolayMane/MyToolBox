#!/usr/env/python2.7

import sys, time

prot_file = open(sys.argv[1], "r")			# cog-20.fa (note: unzipped)
cog_file = open(sys.argv[2], "r")			# cog-20.cog.csv
cog_trans_file = open(sys.argv[3], "r")		# cog-20.def.tab
outfile = open("merged_cogs.fa", "w")



# Building the dictionary to compare COGs to the GI ID
cog_db = {}
t0 = time.clock()

for line in cog_file:
	split = line.split(",")
        cog_db[split[2]] = split[7]		# GI ID == COG ID, in the COG2020 the position 2 and 7 

cog_file.close()
t1 = time.clock()

print "Cog file read.  Time elapsed: " + str(t1-t0) + " seconds."

# Building the dictionary to add the function code to the COGs
trans_cog_db = {}

for line in cog_trans_file:
	trans_cog_db[line.split("\t")[0]] = line.split("\t")[1]
trans_cog_db_file.write(str(trans_cog_db))
cog_trans_file.close()

# Using the dictionary to write to the outfile the protein sequences with COG info
error_count = 0
for line in prot_file:
	if line[0] == ">":
		raw_gi_id = line.strip().split(" ")[0]# in th cog2020 .fa file we have spaces rather than "|"
                gi_id = raw_gi_id.replace(">","").replace("_1",".1") # to replace ">" and "_1" and to add ".1" in order to match cog_db
		try:
			outfile.write(line.strip() + " | " + cog_db[gi_id] + " | " + trans_cog_db[cog_db[gi_id]] + "\n")
		except KeyError:
			error_count += 1
			outfile.write(line.strip() + " | NO COG FOUND | NA\n")
			continue
	else:
		outfile.write(line)
t2 = time.clock()
prot_file.close()
outfile.close()

print "Protein file analyzed.  Time elapsed: " + str(t2-t1) + " seconds."
print "Number of sequences without a COG: " + str(error_count)
